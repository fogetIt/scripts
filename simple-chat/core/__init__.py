# -*- coding: utf-8 -*-
# @Date:   2018-01-19 18:51:46
# @Last Modified time: 2018-01-19 18:52:00
import json
import socket

from .client_store import ClientStore
from .logger import Logger
from .mixin import Single


PORT = 8888
BUFFER_SIZE = 4096
LISTEN_NUMBER = 15
SELECT_TIMEOUT = 3
SERVER_TIMEOUT = None


class ServerSocket(Single):

    def __init__(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(SERVER_TIMEOUT)
        server_socket.bind(("0.0.0.0", PORT))
        server_socket.listen(LISTEN_NUMBER)


class Server(ServerSocket):

    def close(self):
        pass

    def parser(self, client_ip=None, client_socket=None):
        message = self.receive_message(client_ip=client_ip, client_socket=client_socket)
        if not message:
            return "socket error"
        try:
            return json.loads(message)
        except Exception as e:
            print(e)
            return "message formatting error"