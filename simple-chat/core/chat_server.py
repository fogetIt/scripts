# -*- coding: utf-8 -*-
# @Date:   2018-01-20 17:14:06
# @Last Modified time: 2018-01-20 17:14:28
import socket
from .mixin import Single
from .logger import Logger
from .client_store import ClientStore


PORT = 8888
BUFFER_SIZE = 4096
LISTEN_NUMBER = 15
SERVER_TIMEOUT = None


class ServerSocket(Single):

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(SERVER_TIMEOUT)
        self.server_socket.bind(("0.0.0.0", PORT))
        self.server_socket.listen(LISTEN_NUMBER)


class ChartServer(Logger, ServerSocket, ClientStore):

    def __init__(self):
        Logger.__init__(self)
        ServerSocket.__init__(self)
        ClientStore.__init__(self)

    def close_client(self, client_ip=None, client_socket=None):
        client = self.get_client(client_ip=client_ip, client_socket=client_socket)
        if client:
            client.get("socket").close()
            self.remove_client(client.get("ip"))
            return True
        else:
            self.logger.error("client socket is not exist")
            return False

    def send_message(self, message, receiver=None, receiver_socket=None):
        receiver_client = self.get_client(user_name=receiver, client_socket=receiver_socket)
        if not receiver_client:
            self.logger.error("receiver is not exist")
        elif not message:
            self.logger.error("message empty error")
        else:
            try:
                receiver_client.get("socket").send(message)
                self.logger.info(
                    "send message to {receiver} success".format(
                        receiver=receiver_client.get("user")
                    )
                )
                return True
            except Exception as e:
                self.logger.error(e)
                self.close_client(client_socket=receiver_client.get("socket"))
        return False

    def broadcast(self, message, sender="system", sender_socket=None):
        success = failed = 0
        sender_client = {} if sender == "system" else self.get_client(
            user_name=sender, client_socket=sender_socket
        )
        if type(sender_client) is dict:
            for tcp_socket in self.socket_iterator:
                if tcp_socket != sender_client.get("socket"):
                    result = self.send_message(message, receiver_socket=tcp_socket)
                    if result:
                        success += 1
                    else:
                        failed += 1
        return success, failed

    def receive_message(self, client_ip=None, client_socket=None):
        sender_client = self.get_client(client_ip=client_ip, client_socket=client_socket)
        if sender_client:
            try:
                return sender_client.get("socket").recv(BUFFER_SIZE)
            except Exception as e:
                self.logger.error(e)
                self.close_client(
                    client_ip=sender_client.get("ip"),
                    client_socket=sender_client.get("socket")
                )
        return False
