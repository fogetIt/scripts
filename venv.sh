#!/bin/bash
# @Date:   2018-01-18 16:14:09
# @Last Modified time: 2018-01-18 16:14:29
PSWD=$1

[ $PSWD ] \
&& echo $PSWD | sudo -S echo "running" \
&& virtualenv ./venv/ \
    --system-site-packages \
    -p /usr/bin/python \
&& source ./venv/bin/activate \
&& pip install \
    -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
&& sudo apt-get install \
    libjavascriptcoregtk-4.0-18 \
    libwebkit2gtk-4.0-37 \
    libwebkit2gtk-4.0-37-gtk2 \
    python-wxtools

sudo apt-get -f install -y