# -*- coding: utf-8 -*-
# @Date:   2018-01-20 13:54:13
# @Last Modified time: 2018-01-20 13:54:26


class Single(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Single, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class RouterError(Exception):

    def __init__(self, title=None, err=""):
        if title:
            err = "add router error, router {title} has already existed".format(title=title)
        super(RouterError, self).__init__(err)
