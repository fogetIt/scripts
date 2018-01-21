# -*- coding: utf-8 -*-
# @Date:   2017-03-20 10:52:39
# @Last Modified time: 2017-11-21 11:07:43
import select
from threading import Thread
from views import app

SELECT_TIMEOUT = 3


class AcceptClient(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # TODO  当有客户端连接时，把它加进 store
        while True:
            client_socket, client_address = app.server_socket.accept()
            client_ip = client_address[0]
            app.logger.info("{client_ip} is connected".format(client_ip=client_ip))
            app.find_view("login")(client_ip=client_ip, client_socket=client_socket)


class TransmitData(Thread):

    def __init__(self):
        Thread.__init__(self)

    def handler(self, client_ip=None, client_socket=None):
        message_dict = app.parser(client_ip=client_ip, client_socket=client_socket)
        if not message_dict:
            return
        else:
            sender = app.get_user(client_ip=client_ip)
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
            socket_list = [tcp_socket for tcp_socket in app.socket_iterator] # TODO  阻塞，等待数据输入
            r_list, w_list, x_list = select.select(
                socket_list, [], [], SELECT_TIMEOUT
            )
            for client_socket in r_list:
                client_ip = app.get_ip(client_socket=client_socket)
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
