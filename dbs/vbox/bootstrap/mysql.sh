#!/bin/bash
yum update -y
set -e
set -x
yum makecache fast
pushd /home/vagrant
    wget http://repo.mysql.com/mysql57-community-release-el7-8.noarch.rpm
    rpm -ivh mysql57-community-release-el7-8.noarch.rpm
    yum install mysql-server -y
popd
sed -i '/\[mysqld\]/acharacter_set_server=utf8' /etc/my.cnf
echo '[client]' | tee -a /etc/my.cnf
sed -i '/\[client\]/adefault-character-set=utf8' /etc/my.cnf
systemctl start mysqld

DEFAULT_MYSQL_PASSWORD=$(grep 'password' /var/log/mysqld.log | head -n 1 | awk '{print $NF}')
: <<'COMMIT'
mysqladmin -u root -p"${DEFAULT_MYSQL_PASSWORD}" -password mysql_12315_test
COMMIT
mysql -u root -p"${DEFAULT_MYSQL_PASSWORD}" < $(pwd)/init-mysql.sql --connect-expired-password

echo -n 'mysql:         '
mysql --version
