##### Apache 接口性能评估

|mod                           |requests/sec|
|:-----------------------------|:-----------|
|mod_cgi(ScriptAlias)          |10          |
|mod_python(PythonHandler)     |400         |
|mod_wsgi(WSGIDaemonProcess)   |700         |
|mod_wsgi(.htaccess/SetHandler)|850         |
|mod_wsgi(WSGIScriptAlias)     |900         |


##### Apache mod_wsgi
```conf
<VirtualHost *:80>

    Alias /static to/static
    <Directory to/static>
        Require all granted
    </Directory>

    # wsgi.py 父目录访问权限
    <Directory to/proj/proj>
        # wsgi.py 文件访问权限
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    # 子进程模式：python 解释器被嵌入到 apache 子进程中，和 apache 共享内存
    # WSGIPythonPath to/proj/proj:...　# 指定项目路径

    # 守护进程模式：python 解释器运行在隔离的单独进程中，通过 socket 和 apache 进程通信
    # MPM
    #   winnt 模式：processes=1 threads>1
    #   worker 模式：processes>1 threads>1
    #   preforker 模式：processes>1 threads=1
    # django1.0 以下，非线程安全
    # display-name 后台进程的名字
    WSGIDaemonProcess site1 python-home=to/venv python-path=to/proj1 processes=1 threads=15 display-name=%{GROUP}
    WSGIProcessGroup site1
    WSGIScriptAlias url1 to/proj1/proj1/wsgi.py  # url 映射文件系统

    WSGIDaemonProcess site2 python-home=to/venv python-path=to/proj2 processes=1 threads=15 display-name=%{GROUP}
    WSGIProcessGroup site2
    WSGIScriptAlias url2 to/proj2/proj2/wsgi.py
</VirtualHost>
```