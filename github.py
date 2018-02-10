# -*- coding: utf-8 -*-
# @Date:   2016-09-22 09:31:01
# @Last Modified time: 2018-01-31 10:52:28
#
# PATH:${Git}\cmd;
import os
import platform
import time


class Git:

    def __init__(self, my_dir):
        self.parent_path = os.path.abspath("..")
        dir_list = [
            'free-spider',
            'smart-sso',
            'nodeSpider',
            'scripts',
            'LANchat',
            'env',
        ]
        if my_dir == '':
            for i in dir_list:
                self.run(i)
        else:
            self.run(my_dir)

    def pull(self):
        print('nothing to commit')
        os.system('git pull origin master')

    def commit(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print('commiting......')
        os.system('git add --all')
        os.system('git commit -m "%s"' % now)
        os.system('git pull origin master')
        os.system('git push origin master')

    def auto_git(self, _dir):
        info = 1
        if platform.system() == "Windows":
            """
            print info
            0 正确运行
            1 小问题
            2 大问题
            """
            info = os.system('git status | find "nothing to commit" >nul')
        elif 'Ubuntu' in platform.platform():
            file = os.popen('git status')
            output = file.read()
            if "nothing to commit" in output or "无文件要提交" in output:
                info = 0
        if info == 0:
            self.pull()
        elif info == 1:
            self.commit()
        else:
            print('ERROR')
        print('%s>>>%s' % ("-" * 40, _dir))

    def run(self, _dir):
        # _path = self.parent_path + '\\' + _dir
        _path = os.path.join(self.parent_path, _dir)
        print(_path)
        # os.system('cd %s' % _path) # 无法切换工作目录
        os.chdir(_path)
        # print os.getcwd()
        self.auto_git(_dir)


if __name__ == '__main__':
    my_dir = raw_input(">>>")
    git = Git(my_dir)
