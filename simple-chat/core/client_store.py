# -*- coding: utf-8 -*-
# @Date:   2018-01-19 10:54:33
# @Last Modified time: 2018-01-19 10:55:27
from bidict import bidict
from .mixin import Single


class ClientStore(Single):

    def __init__(self):
        self.user_ip_dict = bidict()
        self.ip_socket_dict = bidict()

    def add_client(self, user_name=None, client_ip=None, client_socket=None):
        if user_name in self.user_ip_dict or client_ip in self.ip_socket_dict:
            return "{user_name} or {client_ip} is already exist".format(
                user_name=user_name, client_ip=client_ip
            )
        self.user_ip_dict.update({user_name: client_ip})
        self.ip_socket_dict.update({client_ip: client_socket})
        return None

    def remove_client(self, client_ip):
        self.user_ip_dict.inv.pop(client_ip)
        self.ip_socket_dict.pop(client_ip)

    def get_client(self, user_name=None, client_ip=None, client_socket=None):
        if not user_name:
            user_name = self.get_user(client_ip=client_ip, client_socket=client_socket)
        if not client_ip:
            client_ip = self.get_ip(user_name=user_name, client_socket=client_socket)
        if not client_socket:
            client_socket = self.get_socket(user_name=user_name, client_ip=client_ip)
        if not client_socket:
            return False
        return {"user": user_name, "ip": client_ip, "socket": client_socket}

    def get_user(self, client_ip=None, client_socket=None):
        user_name = None
        if not client_ip and client_socket:
            client_ip = self.get_ip(client_socket=client_socket)
        if client_ip:
            user_name = self.user_ip_dict.inv.get(client_ip)
        return user_name

    def get_ip(self, user_name=None, client_socket=None):
        client_ip = None
        if user_name:
            client_ip = self.user_ip_dict.get(user_name)
        elif client_socket:
            client_ip = self.ip_socket_dict.inv.get(client_socket)
        return client_ip

    def get_socket(self, user_name=None, client_ip=None):
        client_socket = None
        if not client_ip and user_name:
            client_ip = self.get_ip(user_name=user_name)
        if client_ip:
            client_socket = self.ip_socket_dict.get(client_ip)
        return client_socket

    @property
    def socket_iterator(self):
        return self.ip_socket_dict.itervalues()

    @property
    def user_list(self):
        return self.user_ip_dict.keys()
