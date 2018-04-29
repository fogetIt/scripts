#!/bin/bash
# @Date:   2017-12-22 09:55:32
# @Last Modified time: 2017-12-26 14:02:26
password=$1

if [ $password ]; then
    echo $password | sudo -S echo $password
    sudo apt-get install postgresql -y
    sudo apt-get install postgresql-client -y
    # GUI
    sudo apt-get install pgadmin3 -y
    sudo npm install -g less less-plugin-clean-css
    sudo apt-get install node-less -y

    if [ ! -d ./odoo/ ]; then
        git clone https://github.com/odoo/odoo.git
    fi

    virtualenv --version
    if [ $? != 0 ]; then
        pip install virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple
    fi

    if [ ! -d ./venv/bin ]; then
        virtualenv ./venv --no-site-packages -p /usr/bin/python
    fi

    source ./venv/bin/activate
    if [ $? == 0 ]; then
        cd odoo
        sudo python setup.py install

        # lxml depended
        sudo apt-get -y install libxml2-dev libxslt-dev python-dev
        # pyldap depended
        sudo apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev

        pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    fi
    deactivate
else
    echo "need password"
fi

: "
# 切换到 postgres 用户（系统用户，密码随机）
sudo su - postgres

# 以同名数据库用户的身份，登录 postgres 数据库
psql postgres

sudo -u postgres psql postgres

# 修改密码
ALTER USER postgres WITH PASSWORD '123zhang';
# 增加权限
ALTER USER zdd WITH CREATEDB;
"


: "
# 创建用户
sudo adduser odoo

# 创建超级用户
sudo -u postgres createuser --superuser odoo
CREATE ROLE zdd SUPERUSER;

sudo su - odoo
psql

# 创建数据库用户
CREATE USER zdd WITH PASSWORD '123zhang';

# 创建用户数据库，指定所有者，授权
CREATE DATABASE odoo_oa OWNER zdd;
GRANT ALL PRIVILEGES ON DATABASE odoo_oa to zdd;
"