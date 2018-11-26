# coding: utf-8
# from selenium import webdriver
# browser = webdriver.Chrome()
#
# browser.get('http://money.finance.sina.com.cn/quotes_service/view/qihuohangqing.html')
# title = browser.title
# print(browser.title)
# # print(browser.page_source)
# browser.close()


#!/usr/bin/env python
# coding:utf-8

import os
import base64
import sys


def baseurl(argv):
    """
    thunder://... -> http://...
    """
    if len(argv) == 2:
        url = argv[1]
    else:
        print("Input Error!\n usage: %s 'url'" % (argv[0]))
        sys.exit(1)
    if url.startswith('thunder://'):
        url = url[10:]+'\n'
        url = base64.decodestring(url)
        url = url[2:-2]
    elif url.startswith('flashget://'):
        url = url[11:url.find('&')]+'\n'
        url = base64.decodestring(url)
        url = url[10:-10]
    elif url.startswith('qqdl://'):
        url = url[7:]+'\n'
        url = base64.decodestring(url)
    else:
        print('\n It is not a available url!!')
    return url

# www.iplaypy.com


def test():
    # url = 'thunder://QUFodHRwOi8veDEwMi51dW5pYW8uY29tOjEwMS9kYXRhL2Jicy51dW5pYW8uY29tJUU2JTgyJUEwJUU2JTgyJUEwJUU5JUI4JTlGLyVFNyU5QiU5NyVFNiVBMiVBNiVFNyVBOSVCQSVFOSU5NyVCNC0lRTYlODIlQTAlRTYlODIlQTAlRTklQjglOUYlRTQlQjglQUQlRTYlOTYlODclRTUlQUQlOTclRTUlQjklOTUucm12Ylpa'
    p = baseurl(sys.argv)
    print(p)

if __name__ == '__main__':
    test()
