# -*- coding: utf-8 -*-
# @Date:   2018-01-20 14:59:10
# @Last Modified time: 2018-01-20 14:59:46
import json
import socket
from .client_store import ClientStore
from .logger import Logger
from message import Message


class BaseServer(Logger, ClientStore, Message):

    def __init__(self):
        Logger.__init__(self)

    def close_client(self, client_ip=None, client_socket=None):
        if not client_socket and client_ip:
            client_socket = self.get_socket(client_ip=client_ip)
        elif not client_ip and client_socket:
            client_ip = self.get_ip(client_socket=client_socket)
        if client_socket:
            client_socket.close()
            self.remove_client(client_ip)
            self.broadcast(
                self.user_list_message(self.get_user_list())
            )
        else:
            self.logger.error("client socket is not exist")
        return False

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
                self.close_client(client_socket=receiver_socket)

    def broadcast(self, message, sender=None, sender_socket=None):
        if not sender_socket and sender:
            sender_socket = self.get_socket(user_name=sender)
        if sender_socket:
            for tcp_socket in self.get_socket_list():
                if tcp_socket != sender_socket:
                    self.send_message(message, sender=sender,
                                      receiver_socket=tcp_socket)

    def receive_message(self, client_ip=None, client_socket=None):
        try:
            return client_socket.recv(BUFFER_SIZE)
        except Exception as e:
            self.logger.error(e)
            self.close_client(client_ip=client_ip, client_socket=client_socket)
            return None
