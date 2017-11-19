# -*- coding: utf-8 -*-
# @Date:   2017-11-15 11:48:15
# @Last Modified time: 2017-11-15 13:31:44
"""
端口扫描器
"""
import time
import socket
import logging


socket.setdefaulttimeout(3)


class Scan(object):
    scan_logger = logging.getLogger("file")
    scan_logger.setLevel(logging.INFO)
    scan_logger.addHandler(logging.FileHandler("scan.log"))

    @staticmethod
    def error(msg):
        print("\033[1;31;40m %s \033[0m" % msg)

    @staticmethod
    def info(msg):
        print("\033[1;32;40m %s \033[0m" % msg)

    def time_decorator(func):
        """
        use decorator in class
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            Scan.info(str(end_time - start_time))
        return wrapper

    def scan(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((ip, port))
            if result == 0:
                self.scan_logger.info("%s:%s" % (ip, port))
                self.info("%s:%s 端口开放" % (ip, port))
            s.close()
        except Exception as e:
            self.error("%s: %s %s" % (ip, port, e))

    @time_decorator
    def __call__(self, ip="127.0.0.1"):
        port = 0
        while True:
            if port >= 65535:
                self.info("端口扫描结束 0~65535")
                break
            self.scan(ip, port)
            port += 1


class GetIpList(object):

    @staticmethod
    def ip2num(ip):
        """
        << 是位移
        << 右移一个就是 * 2 意思就是 ip[0]*2^24 + ip[1]*2^16 + ip[2]*2^8 + ip[3]
        ipv4地址，是一个32位的二进制数，每8位转换成十进制，就是普通看到的那种形式了
        """
        ip = [int(x) for x in ip.split('.')]
        return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

    @staticmethod
    def num2ip(num):
        return '%s.%s.%s.%s' % (
            (num & 0xff000000) >> 24,
            (num & 0x00ff0000) >> 16,
            (num & 0x0000ff00) >> 8,
            num & 0x000000ff
        )

    def __call__(self, start_ip, end_ip):
        return [
            self.num2ip(num) for num in range(
                self.ip2num(start_ip),
                self.ip2num(end_ip) + 1
            ) if num & 0xff
        ]


def main(start_ip="127.0.0.1", end_ip="127.0.1.1"):
    for ip in GetIpList()(start_ip, end_ip):
        Scan()(ip)


if __name__ == '__main__':
    main()
