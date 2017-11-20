# -*- coding: utf-8 -*-
# @Date:   2017-03-20 10:52:39
# @Last Modified time: 2017-03-20 13:44:44
import json
import socket
import select
import hashlib
import logging.config
from threading import Thread
from bidict import bidict


PORT = 8888
LISTEN_NUM = 15
BUFFER_SIZE = 4096
SELECT_TIMEOUT = 3
SERVER_TIMEOUT = None
logging.config.fileConfig("logger.conf")


class ColorsUtils(object):

    def create_color_str(self, display, fg_color, bg_color, message):
        return "\033[%s;%s;%sm %s \033[0m" % (
            display, fg_color, bg_color, message
        )

    def warn_message(self, message):
        return self.create_color_str(1, 33, 40, message)

    def info_message(self, message):
        return self.create_color_str(1, 32, 40, message)


class LogUtils(ColorsUtils, logging.Filter):
    inm = ColorsUtils.info_message
    wam = ColorsUtils.warn_message

    def __init__(self, name="server"):
        ColorsUtils.__init__(self)
        self.logger = logging.getLogger(name)
        self.logger.handlers[0].addFilter(self)  # TODO

    def filter(self, record):
        return record.levelno < logging.ERROR


class Chat(LogUtils):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(SERVER_TIMEOUT)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(LISTEN_NUM)
    # data store
    conn_dict = bidict()
    user_dict = bidict()

    def __init__(self):
        LogUtils.__init__(self)

    def update_data_store(self, user_name, client_ip, tcp_socket):
        if user_name in self.user_dict or client_ip in self.conn_dict:
            self.logger.warn(self.wam("%s or %s is already exist" % (user_name, client_ip)))
            self.close_socket(client_ip=client_ip)
        self.user_dict.update({user_name: client_ip})
        self.conn_dict.update({client_ip: tcp_socket})

    @staticmethod
    def create_message(title, ext_data=None, sender="system"):
        """
        :param title:
            login
            user_list
            private
            public
        :param ext_data:
        :param sender:
            system
            user_name
        :return:
        """
        message_dict = {"title": title, "sender": sender}
        if ext_data:
            message_dict.update(ext_data)
        return json.dumps(message_dict)

    def broadcast_user_list(self):
        user_list = self.user_dict.keys()
        if user_list:
            self.broadcast(
                self.create_message("user_list", {"user_list": user_list})
            )
        else:
            self.logger.warn(self.wam("user_list is empty"))

    def broadcast(self, message, sender=None):
        """
        广播
        """
        sender_socket = self.conn_dict.get(sender) if sender else None
        for tcp_socket in self.conn_dict.itervalues():
            if tcp_socket != sender_socket:
                self.send_to_user(tcp_socket, message)

    def send_to_user(self, tcp_socket=None, message=None, client_ip=None):
        """
        发送给特定用户
        """
        if not tcp_socket:
            if client_ip:
                tcp_socket = self.conn_dict.get(client_ip)
            else:
                self.logger.error("tcp_socket and client_ip are all empty")
        if tcp_socket:
            if not client_ip:
                client_ip = self.conn_dict.inv.get(tcp_socket)
            try:
                tcp_socket.send(message)
                self.logger.info(
                    self.inm("send message to %s success" % client_ip))
            except Exception, e:
                self.logger.error(e)
                self.close_socket(tcp_socket)  # TODO
        else:
            self.logger.error("tcp_socket is not exist")

    def close_socket(self, tcp_socket=None, client_ip=None):
        if not tcp_socket:
            if client_ip:
                tcp_socket = self.conn_dict.get(client_ip)
        if tcp_socket:
            tcp_socket.close()
            self.conn_dict.pop(client_ip)
            self.user_dict.inv.pop(client_ip)
            self.broadcast_user_list()  # TODO
        else:
            self.logger.error("tcp_socket is not exist")


class AcceptClient(Thread, Chat):

    def __init__(self):
        Thread.__init__(self)
        Chat.__init__(self)

    def login(self, tcp_socket, client_ip):
        try:
            message = tcp_socket.recv(BUFFER_SIZE)
            if message:
                try:
                    message_dict = json.loads(message)
                    title = message_dict.get("title")

                    name = message_dict.get("name")
                    password = message_dict.get("password")

                    error_text = None
                    if not title or title != "login":
                        error_text = "data title error"
                    elif not name or not password:
                        error_text = "while title is login, name and password can't empty"
                    elif not self.check_password(name, password):
                        error_text = "user is not registered"
                    else:
                        self.update_data_store(
                            name, client_ip, tcp_socket
                        )

                    if error_text:
                        self.logger.warn(self.wam(error_text))
                        self.send_to_user(
                            tcp_socket,
                            self.create_message(
                                "error", {"error_text": error_text}
                            )
                        )
                    else:
                        # TODO
                        # 广播在线用户
                        self.broadcast_user_list()
                        self.logger.info(self.inm("%s login successful" % client_ip))
                except Exception, e:
                    self.logger.error("data in wrong format")
                    self.logger.error(e)
        except Exception, e:
            self.logger.error(e)
            self.close_socket(tcp_socket)

    def check_password(self, name, password):
        with open("password.json", "r") as reader:
            _dict = json.loads(reader.read())
            if name in _dict:
                m = hashlib.md5()
                m.update(name)
                m.update(password)
                if m.hexdigest() == _dict.get(name):
                    return True
            return False

    def run(self):
        # TODO  当有客户端连接时，把它加进 conn_list
        while True:
            tcp_socket, client_address = self.server_socket.accept()
            client_ip = client_address[0]
            self.logger.info(self.inm("client %s connected" % client_ip))
            self.login(tcp_socket, client_ip)


class TransmitData(Thread, Chat):

    def __init__(self):
        Thread.__init__(self)
        Chat.__init__(self)

    def logout(self, sender_socket, sender_ip):
        self.close_socket(tcp_socket=sender_socket, client_ip=sender_ip)

    def send_to_one(self, sender, text, receiver):
        message = self.create_message("private", {"text": text}, sender=sender)
        self.send_to_user(message=message, client_ip=receiver)

    def send_to_all(self, sender, text):
        message = self.create_message("public", {"text": text}, sender=sender)
        self.broadcast(message, sender=sender)

    def distribute(self, sender_socket, sender_ip, sender, message_dict):
        """
        ignore title == "login"
        """
        title = message_dict.get("title")
        text = message_dict.get("text")
        if not title:
            self.logger.warn(self.wam("data title is empty"))
        elif title == "logout":
            self.logout(sender_socket, sender_ip)
        elif not text:
            self.logger.warn(self.wam("data text is empty"))
        elif title == "send_to_one":
            send_to = message_dict.get("send_to")
            if not send_to:
                self.logger.error(
                    "while title is send_to_one, send_to can't be empty")
            else:
                receiver = self.user_dict.get(send_to)
                if sender == receiver:
                    self.logger.warn(self.wam("can't send message to self"))
                else:
                    self.send_to_one(sender, text, receiver)
        elif title == "send_to_all":
            self.send_to_all(sender, text)

    def receive_message_and_distribute(self, sender_socket, sender_ip):
        try:
            message = sender_socket.recv(BUFFER_SIZE)
            if message:
                try:
                    message_dict = json.loads(message)
                    sender = self.user_dict.inv.get(sender_ip)
                    if not sender:
                        self.logger.error("sender %s is not online" % sender)
                    else:
                        self.distribute(sender_socket, sender_ip,
                                        sender, message_dict)
                except Exception, e:
                    self.logger.error("data in wrong format")
                    self.logger.error(e)
        except Exception, e:
            self.logger.error(e)
            self.close_socket(sender_socket)

    def run(self):
        while True:
            conn_list = [tcp_socket for tcp_socket in self.conn_dict.values()]
            # TODO  阻塞，等待数据输入
            r_list, w_list, x_list = select.select(
                conn_list, [], [], SELECT_TIMEOUT)
            for tcp_socket in r_list:
                client_ip = self.conn_dict.inv.get(tcp_socket)  # TODO
                self.receive_message_and_distribute(tcp_socket, client_ip)


def main():
    accept_client = AcceptClient()
    transmit_data = TransmitData()
    accept_client.daemon = True
    transmit_data.daemon = True
    accept_client.start()
    transmit_data.start()
    jobs = [accept_client, transmit_data]
    for j in jobs:
        j.join()


if __name__ == '__main__':
    print("simple chat server listening 0.0.0.0:%s" % PORT)
    main()
