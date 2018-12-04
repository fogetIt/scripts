版本
=========
:MySQL Community Server: 社区开源版，不提供官方技术支持
:MySQL Enterprise Edition: 企业版本，可以试用30天
:MySQL Cluster: 开源集群版，可将几个 MySQL Server 封装成一个
:MySQL Cluster CGE: 高级集群版，需付费

GUI
====
- phpMyAdmin
- Navicat for MySQL(收费)
- MySQL Workbench(官方)

    :MySQL Workbench OSS: 社区版
    :MySQL Workbench SE: 商用版

- MySQL ODBC Connector
- SQLyog(win/收费)
- DBeaver(收费)

**mysql 解压包里面的源文件和 debug 等文件都没有删掉， dubug 文件和 pdf 文件可以删。**

安装
======
- windows ZIP Archive
    - 解压到想安装的地方
    - 配置环境变量—— bin 文件夹
    - 以管理员身份打开命令窗口

        :安装服务: mysqld --install
        :删除服务: mysqld --remove
        :输出错误信息: mysqld --console

    - windows 免安装最新版没有 data 目录，没有用户、权限、密码等配置
        .. code:: bat

            mysqld --initialize-insecure  :: 生成无密码 root 用户
            mysqld --initialize           :: 生成随机密码 root 用户
            mysqld --skip-grant-tables    :: 关闭权限检查
            net start mysql
            net stop mysql
- `centos <./vbox/bootstrap/mysql.sh>`_
    - 默认 mysql-server 已换成 mariadb ，用法与　mysql 没有区别
        .. code:: bash

            systemctl start mariadb
            systemctl stop mariadb
            systemctl restart mariadb
            systemctl enable mariadb
- ubuntu
    .. code:: bash

        sudo apt install -y mysql-server mysql-client

字符集
=============
.. code:: mysql

    # 查看字符集
    show variables like '%collation%';
    show variables like 'character_set_%';
    # character_set_client       客户编码
    # character_set_connection   建立连接使用的编码
    # character_set_database     数据库编码
    # character_set_results      结果集编码
    # character_set_server       数据库服务器编码
    # character_set_filesystem
    # character_set_system
    # character_sets_dir

    # 动态设置数据库字符集(重启会失效)
    SET character_set_client = utf8;
    SET character_set_connection = utf8;
    SET character_set_database = utf8;
    SET character_set_results = utf8;
    SET character_set_server = utf8;

**mysql 命令不区分大小写。以 ; 作为命令结束符；以 \c 取消命令；引号( ' or " )可以跨行，引号内部 ; 和 \c 无效。**
