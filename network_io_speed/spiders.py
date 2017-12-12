# -*- coding: utf-8 -*-
# @Date:   2017-03-13 17:55:27
# @Last Modified time: 2017-11-15 17:15:12
import time
import socket
import logging
import logging.config
import urllib2
from threading import Thread
from functools import partial
from multiprocessing import Pool, Manager

"""
Set global default timeout.
There's no need to set timeout in urllib2.urlopen().
"""
socket.setdefaulttimeout(3)
CONCURRENT_NUM = 10  # 并发量
REPEAT_TIMES = 1     # 重复请求次数

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '%(asctime)s \033[1;32;40m %(message)s \033[0m',
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '__logger': {
            'level': 'DEBUG',
            'handlers': ['null'],
            'propagate': True
        }
    }
})


class LogDecorator(object):
    """
    装饰器，经常被用于有切面需求的场景（插入日志、性能测试、事务处理等）
    """
    __logger = logging.getLogger('__logger')

    def __init__(self, func):
        self.func = func

    @staticmethod
    def get_current_timestamp():
        return time.time()

    def __get__(self, obj, obj_type):
        """
        Transmit obj(class instance) to self.__call__().
        Only work while this class as other class's attr.
        """
        return partial(self.__call__, obj)

    def __call__(self, *args, **kwargs):
        """
        make instance callable as a function(class decorator must have __call__)
        wrapper(*args, **kwargs) accept all arguments
        """
        start_time = self.get_current_timestamp()
        self.func(*args, **kwargs)
        end_time = self.get_current_timestamp()
        self.__logger.info(str(end_time - start_time))


class SimpleSpider(object):

    def __init__(self, url_list):
        self.url_list = []
        for i in range(REPEAT_TIMES):
            self.url_list.extend(url_list)

    @LogDecorator
    def main(self):
        for url in self.url_list:
            self.get_html(url)

    def get_html(self, url):
        try:
            resp = urllib2.urlopen(url)
            # print[resp.getcode(), url]
        except Exception as e:
            print[e, url]


class ThreadSpider(Thread, SimpleSpider):
    __S = set()

    def __init__(self, url_list):
        Thread.__init__(self)
        SimpleSpider.__init__(self, url_list)

    @staticmethod
    @LogDecorator
    def main(url_list):
        t_list = [ThreadSpider(url_list) for i in range(CONCURRENT_NUM)]
        for t in t_list:
            t.start()
        for t in t_list:
            t.join()

    def run(self):
        for url in self.url_list:
            if url not in self.__S:
                self.__S.add(url)
                self.get_html(url)


class GeventSpider(SimpleSpider):
    __S = set()

    def __init__(self, url_list):
        super(GeventSpider, self).__init__(url_list)

    def run(self):
        for url in self.url_list:
            if url not in self.__S:
                self.__S.add(url)
                self.get_html(url)

    @LogDecorator
    def main(self):
        import gevent
        from gevent import monkey
        monkey.patch_socket()
        monkey.patch_ssl()  # 加密
        gevent.joinall([
            gevent.spawn(self.run) for i in range(CONCURRENT_NUM)
        ])


class ProcessSpider(SimpleSpider):
    __S = Manager().dict()

    def __init__(self, url_list):
        super(ProcessSpider, self).__init__(url_list)

    def run(self):
        for url in self.url_list:
            if url not in self.__S:
                self.__S.update({url: True})
                self.get_html(url)


def p_start(url_list):
    psp = ProcessSpider(url_list)
    psp.run()


@LogDecorator
def psp(url_list):
    pool = Pool(processes=CONCURRENT_NUM)
    for i in range(CONCURRENT_NUM):
        pool.apply_async(
            p_start,
            args=(url_list,)
        )
    pool.close()
    pool.join()
