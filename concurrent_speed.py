# -*- coding: utf-8 -*-
# @Date:   2017-03-13 17:55:27
# @Last Modified time: 2017-11-15 17:15:12
import re
import time
import socket
import logging
import logging.config
import urllib2
from threading import Thread
from functools import partial
from multiprocessing import Pool, Manager
from bs4 import BeautifulSoup as soup


"""
Set global default timeout.
There's no need to set timeout in urllib2.urlopen().
"""
socket.setdefaulttimeout(3)

REPEAT_NUMBER = 1       # 重复请求次数
CONCURRENT_NUMBER = 10  # 并发量

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


class LoggingDecorator(object):
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
        Make instance callable as a function(class decorator must have __call__)
        wrapper(*args, **kwargs) accept all arguments
        """
        start_time = self.get_current_timestamp()
        self.func(*args, **kwargs)
        end_time = self.get_current_timestamp()
        self.__logger.info(str(end_time - start_time))


def generate_url_list():
    start_url = "https://www.hao123.com"
    resp = urllib2.urlopen(start_url)
    html = resp.read()
    resp.close()
    root_tag = soup(html)
    tag_list = root_tag.findAll(name="a", attrs={"href": re.compile(".*")})
    url_list = []
    for i in tag_list:
        url = i.get("href")
        if url not in ["#", "javascript:;"]:
            if not url.startswith("http"):
                url = start_url + url
            url_list.append(url)
    return url_list


class SimpleSpider(object):

    def __init__(self, url_list):
        self.url_list = []
        for i in range(REPEAT_NUMBER):
            self.url_list.extend(url_list)

    @LoggingDecorator
    def main(self):
        for url in self.url_list:
            self.get_html(url)

    def get_html(self, url):
        try:
            resp = urllib2.urlopen(url)
            # print[resp.getcode(), url]
            resp.close()
        except Exception as e:
            print[e, url]


class ThreadSpider(Thread, SimpleSpider):
    __S = set()

    def __init__(self, url_list):
        Thread.__init__(self)
        SimpleSpider.__init__(self, url_list)

    @staticmethod
    @LoggingDecorator
    def main(url_list):
        t_list = [ThreadSpider(url_list) for i in range(CONCURRENT_NUMBER)]
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

    @LoggingDecorator
    def main(self):
        import gevent
        from gevent import monkey
        monkey.patch_socket()
        monkey.patch_ssl()  # 加密
        gevent.joinall([
            gevent.spawn(self.run) for i in range(CONCURRENT_NUMBER)
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

def process_start(url_list):
    psp = ProcessSpider(url_list)
    psp.run()


@LoggingDecorator
def main_process(url_list):
    pool = Pool(processes=CONCURRENT_NUMBER)
    for i in range(CONCURRENT_NUMBER):
        pool.apply_async(
            process_start,
            args=(url_list,)
        )
    pool.close()
    pool.join()


if __name__ == '__main__':
    url_list = generate_url_list()
    SimpleSpider(url_list).main()
    ThreadSpider.main(url_list)
    GeventSpider(url_list).main()
    main_process(url_list)
