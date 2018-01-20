# -*- coding: utf-8 -*-
# @Date:   2018-01-19 15:18:28
# @Last Modified time: 2018-01-19 15:18:35
import json


class Message(object):

    @classmethod
    def create(cls, sender=None, title=None, **ext_data):
        if not sender or not title:
            return None
        message_dict = {"title": title, "sender": sender}
        if ext_data:
            message_dict.update(ext_data)
        return json.dumps(message_dict)

    @classmethod
    def private_message(cls, sender=None, text=None):
        if not text:
            return None
        return cls.create(sender=sender, title="private", text=text)

    @classmethod
    def group_message(cls, sender=None, text=None):
        if not text:
            return None
        return cls.create(sender=sender, title="group", text=text)

    @classmethod
    def user_list_message(cls, user_list=None):
        if not user_list:
            return None
        return cls.create(sender="system", title="refresh", user_list=user_list)

    @classmethod
    def login_error_message(cls, text=None):
        if not text:
            return None
        return cls.create(sender="system", title="error", text=text)
