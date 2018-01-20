# -*- coding: utf-8 -*-
# @Date:   2017-03-20 10:52:39
# @Last Modified time: 2017-11-21 11:07:43
import hashlib
import json
import select
import socket
from threading import Thread

from client_store import Store
from logger import Logger

from message import Message

PORT = 8888
BUFFER_SIZE = 4096
LISTEN_NUMBER = 15
SELECT_TIMEOUT = 3
SERVER_TIMEOUT = None


class Server(Logger, Store, Message):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(SERVER_TIMEOUT)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(LISTEN_NUMBER)

    def __init__(self):
        Logger.__init__(self)

    def refresh_user_list(self):
        user_list = self.get_user_list()
        if user_list:
            self.broadcast(self.refresh_user_list_message(user_list))
        else:
            self.logger.warning("user list is empty")

    def close_socket(self, client_ip=None, client_socket=None):
        if not client_socket and client_ip:
            client_socket = self.get_socket(client_ip=client_ip)
        elif not client_ip and client_socket:
            client_ip = self.get_ip(client_socket=client_socket)
        if client_socket:
            client_socket.close()
            self.remove_client(client_ip)
            self.refresh_user_list()
        else:
            self.logger.error("client socket is not exist")

    def send_message(self, message, sender="system", receiver=None, receiver_socket=None):
        if not receiver_socket and receiver:
            receiver_socket = self.get_socket(user_name=receiver)
        elif not receiver and receiver_socket:
            receiver = self.get_user(client_socket=receiver_socket)
        if not receiver_socket:
            self.logger.error("receiver is not exist")
        elif not message:
            self.logger.error("message empty error")
        else:
            try:
                receiver_socket.send(message)
                self.logger.info(
                    "{sender} send message to {receiver} success".format(
                        sender=sender, receiver=receiver
                    )
                )
            except Exception as e:
                self.logger.error(e)
                self.close_socket(client_socket=receiver_socket)

    def broadcast(self, message, sender=None, sender_socket=None):
        if not sender_socket and sender:
            sender_socket = self.get_socket(user_name=sender)
        if sender_socket:
            for tcp_socket in self.get_socket_list():
                if tcp_socket != sender_socket:
                    self.send_message(message, sender=sender, receiver_socket=tcp_socket)

    def receive_message(self, client_ip=None, client_socket=None):
        try:
            return client_socket.recv(BUFFER_SIZE)
        except Exception as e:
            self.logger.error(e)
            self.close_socket(client_ip=client_ip, client_socket=client_socket)
            return None

    def parser(self, client_ip=None, client_socket=None):
        message = self.receive_message(client_ip=client_ip, client_socket=client_socket)
        if not message:
            return "socket error"
        try:
            return json.loads(message)
        except Exception as e:
            print(e)
            return "message formatting error"


class AcceptClient(Thread, Server):

    def __init__(self):
        Thread.__init__(self)
        Server.__init__(self)

    def login(self, client_ip=None, client_socket=None):
        message_dict = self.parser(client_ip=client_ip, client_socket=client_socket)
        if type(message_dict) is not dict:
            result = message_dict
        elif message_dict.get("title") != "login":
            result = "title error"
        else:
            name = message_dict.get("name")
            password = message_dict.get("password")
            if not self.check_password(name, password):
                result = "name or password error"
            else:
                result = self.add_client(
                    user_name=name,
                    client_ip=client_ip,
                    client_socket=client_socket
                )

        if result:
            self.logger.warning(result)
            self.send_message(self.login_error_message(result))
        else:
            self.refresh_user_list()
            self.logger.info("{client_ip} login successful".format(client_ip=client_ip))

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
        # TODO  当有客户端连接时，把它加进 store
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_ip = client_address[0]
            self.logger.info("{client_ip} is connected".format(client_ip=client_ip))
            self.login(client_ip=client_ip, client_socket=client_socket)


class TransmitData(Thread, Server):

    def __init__(self):
        Thread.__init__(self)
        Server.__init__(self)

    def logout(self, message_dict=None, client_ip=None, client_socket=None):
        self.close_socket(client_ip=client_ip, client_socket=client_socket)

    def send_to_one(self, message_dict=None, client_ip=None, client_socket=None):
        sender = self.get_user(client_ip=client_ip, client_socket=client_socket)
        text = message_dict.get("text")
        receiver = message_dict.get("receiver")
        message = self.private_message(sender=sender, text=text)
        self.send_message(message, sender=sender, receiver=receiver)

    def send_to_all(self, message_dict=None, client_ip=None, client_socket=None):
        sender = self.get_user(client_ip=client_ip, client_socket=client_socket)
        text = message_dict.get("text")
        message = self.group_message(sender=sender, text=text)
        self.broadcast(message, sender=sender)

    def router(self):
        return {
            "logout": self.logout,
            "private": self.send_to_one,
            "group": self.send_to_all
        }

    def handler(self, client_ip=None, client_socket=None):
        message_dict = self.parser(client_ip=client_ip, client_socket=client_socket)
        if type(message_dict) is not dict:
            self.logger.warning(message_dict)
        else:
            sender = self.get_user(client_ip=client_ip)
            if not sender:
                self.logger.error("{sender} is not online".format(sender=sender))
            else:
                view = self.router().get(message_dict.get("title"))
                if not view:
                    self.logger.error("title error")
                else:
                    view(message_dict, client_ip=client_ip, client_socket=client_socket)

    def run(self):
        while True:
            socket_list = [tcp_socket for tcp_socket in self.get_socket_list()]
            # TODO  阻塞，等待数据输入
            r_list, w_list, x_list = select.select(
                socket_list, [], [], SELECT_TIMEOUT
            )
            for client_socket in r_list:
                client_ip = self.get_ip(client_socket=client_socket)  # TODO
                self.handler(client_ip=client_ip, client_socket=client_socket)


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
