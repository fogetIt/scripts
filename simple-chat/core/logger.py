# -*- coding: utf-8 -*-
# @Date:   2018-01-19 10:21:09
# @Last Modified time: 2018-01-19 10:21:18
import logging
import logging.config

if __name__ == "__main__":
    from mixin import Single
else:
    from .mixin import Single


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


class ColoredLogger(Colors, logging.Logger):

    def __init__(self, name):
        logging.Logger.__init__(self, name)

    def info(self, msg, *args, **kwargs):
        message = self.info_message(msg)
        super(ColoredLogger, self).info(message, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        message = self.warn_message(msg)
        super(ColoredLogger, self).warning(message, *args, **kwargs)

    warn = warning


logging.setLoggerClass(ColoredLogger)
if __name__ == "__main__":
    logging.config.fileConfig("logger.conf")
else:
    logging.config.fileConfig("core/logger.conf")


class Logger(Single):

    def __init__(self, name="server"):
        self.logger = logging.getLogger(name)
        self.logger.handlers[0].addFilter(self)  # TODO

    def filter(self, record):
        return record.levelno < logging.ERROR
