# -*- coding: utf-8 -*-
# @Date:   2018-01-19 10:21:09
# @Last Modified time: 2018-01-19 10:21:18
import logging.config
from .mixin import Single

logging.config.fileConfig("logger.conf")


class Colors(object):

    @classmethod
    def create_color_str(cls, display, fg_color, bg_color, message):
        return "\033[%s;%s;%sm %s \033[0m" % (
            display, fg_color, bg_color, message
        )

    @classmethod
    def warn_message(cls, message):
        return cls.create_color_str(1, 33, 40, message)

    @classmethod
    def info_message(cls, message):
        return cls.create_color_str(1, 32, 40, message)


class LoggerClass(Colors, logging.Logger):

    def info(self, msg, *args, **kwargs):
        message = self.info_message(msg)
        super(LoggerClass, self).info(message, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        message = self.warn_message(msg)
        super(LoggerClass, self).warning(message, *args, **kwargs)


class LoggerManager(logging.Manager):

    def getLogger(self, name):
        self.setLoggerClass(LoggerClass)
        return super(LoggerManager, self).getLogger(name)


class Logger(Single):

    def __init__(self, name="server"):
        self.logger = LoggerManager(
            logging.RootLogger(
                logging.WARNING
            )
        ).getLogger(name)
        self.logger.handlers[0].addFilter(self.filter)  # TODO

    def filter(self, record):
        return record.levelno < logging.ERROR
