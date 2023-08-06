#!/bin/sh

mkdir -p /data/logs
mkdir -p /data/logs/admin
mkdir -p /data/logs/server

# nohup python3 -m aioweb --host 0.0.0.0 >> /dev/null 2>&1 &
# nohup python3 server.py start >> /dev/null 2>&1 &

# sslocal -c /etc/shadowsocks.json -d start

# nohup /usr/bin/v2ray -config /etc/v2ray/config.json >> /data/91porn/logs/v2ray.log 2>&1 &
# sh /v2ray.sh start
echo [ $1='prod' ]
if [ -z $1 ];
then
    echo pro env
    cd /admin
    nohup python3 -m aioweb --host 0.0.0.0 --port 8084 >> /data/logs/admin/app.log 2>&1 &
    cd /porn91
    nohup python3 -m aioweb --host 0.0.0.0 >> /data/logs/app.log 2>&1 &
    python3 server.py start -d
    /usr/local/nginx/sbin/nginx
else
    echo dev env
    nohup python -m aioweb --host 0.0.0.0 --port 8082 > /dev/null 2>&1 &
    python server.py start -d

fi

# nginx
# sh
