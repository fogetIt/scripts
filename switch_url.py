#!/usr/bin/env python
# coding: utf-8
import os
import base64
import sys


def thunder2http(url):
    """
    thunder://... -> http://...
    """
    if url.startswith('thunder://'):
        url = url[10:] + '\n'
        url = base64.decodestring(url)
        url = url[2:-2]
    elif url.startswith('flashget://'):
        url = url[11:url.find('&')] + '\n'
        url = base64.decodestring(url)
        url = url[10:-10]
    elif url.startswith('qqdl://'):
        url = url[7:] + '\n'
        url = base64.decodestring(url)
    else:
        print('\n It is not a available url!!')
    return url


def test():
    url = 'thunder://QUFodHRwOi8veDEwMi51dW5pYW8uY29tOjEwMS9kYXRhL2Jicy51dW5pYW8uY29tJUU2JTgyJUEwJUU2JTgyJUEwJUU5JUI4JTlGLyVFNyU5QiU5NyVFNiVBMiVBNiVFNyVBOSVCQSVFOSU5NyVCNC0lRTYlODIlQTAlRTYlODIlQTAlRTklQjglOUYlRTQlQjglQUQlRTYlOTYlODclRTUlQUQlOTclRTUlQjklOTUucm12Ylpa'
    print(thunder2http(url))


if __name__ == '__main__':
    test()
