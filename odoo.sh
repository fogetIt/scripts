#!/bin/bash
# @Date:   2017-12-22 09:55:32
# @Last Modified time: 2017-12-26 14:02:26
set -e
PASSWD=$1

if [ ${PASSWD} ]; then
    echo ${PASSWD} | sudo -S echo ${PASSWD}
    sudo apt-get install postgresql postgresql-client -y
    sudo apt-get install pgadmin3 -y
    sudo npm install -g less less-plugin-clean-css
    sudo apt-get install node-less -y
    [[ -d ./odoo/ ]] || git clone https://github.com/odoo/odoo.git
    [[ virtualenv --version ]] || pip install virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple
    [[ -d ./venv/bin ]] || virtualenv ./venv --no-site-packages -p $(which python)
    # [[ -d ./venv/bin ]] || virtualenv ./venv --system-site-packages -p $(which python)

    source ./venv/bin/activate
        pushd odoo
            sudo python setup.py install
            # lxml depended
            sudo apt-get -y install libxml2-dev libxslt-dev python-dev
            # pyldap depended
            sudo apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev
            pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
        popd
    deactivate
else
    echo "need password"
fi

# sudo apt-get install \
#     libjavascriptcoregtk-4.0-18 \
#     libwebkit2gtk-4.0-37 \
#     libwebkit2gtk-4.0-37-gtk2 \
#     python-wxtools
# sudo apt-get -f install -y


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