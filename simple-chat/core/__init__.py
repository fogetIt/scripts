# -*- coding: utf-8 -*-
# @Date:   2018-01-20 15:20:48
# @Last Modified time: 2018-01-20 15:20:56
import json
import types
from .chat_server import ChartServer
from .mixin import Single, RouterError


class RouterMap(Single):

    def __init__(self):
        self.map = dict()

    def add_rule(self, title, func):
        if self.map.get(title):
            raise RouterError(title=title)
        self.map.update({title: func})

    def find_view(self, title):
        return self.map.get(title)


class App(ChartServer, RouterMap):

    def __init__(self):
        ChartServer.__init__(self)
        RouterMap.__init__(self)

    def parser(self, client_ip=None, client_socket=None):
        message = self.receive_message(client_ip=client_ip, client_socket=client_socket)
        if not message:
            self.logger.error("socket error")
        try:
            return json.loads(message)
        except Exception as e:
            print(e)
            self.logger.error("message formatting error")
        return None

    def parse_message(self, client_ip=None, client_socket=None):
        message_dict = self.parser(client_ip=client_ip, client_socket=client_socket)
        if not message_dict:
            return

    def route(self, title):
        """
        不修改被装饰的函数的行为，只是想获得它的引用
        参照 Flask.route
        :param title:
        :return:
        """
        def decorator(func):
            if not title:
                raise RouterError(err="title empty")
            elif type(func) is not types.FunctionType:
                raise RouterError(err="view func error")
            else:
                self.add_rule(title, func)
            return func
        return decorator
