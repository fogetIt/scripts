# -*- coding: utf-8 -*-
# @Date:   2017-03-13 17:53:13
# @Last Modified time: 2017-08-13 14:32:42
from urls import url_list
from spiders import *


def main():
    sp = SimpleSpider(url_list); sp.main()
    ThreadSpider.main(url_list)
    gsp = GeventSpider(url_list); gsp.main()
    psp(url_list)


if __name__ == '__main__':
    main()
