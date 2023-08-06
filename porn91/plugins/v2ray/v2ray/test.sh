#!/bin/sh

PIDFILE="`pwd`/v2ray.pid"

DAEMON="`pwd`/v2ray_test"
pid=`pidof $DAEMON`
echo $((${#pid}))
# if [ -e $PIDFILE ];then
#     if [ $((${#pid})) -gt 0 ];then
#         if [ "`cat $PIDFILE`" -eq "$pid" ];then
#             echo "kill..."
#         fi
#     fi
# fi


pids=`pidof /home/shadaileng/dev/repo/python/download_91/plugins/v2ray/v2ray/v2ray_test`
for pid in $pids
do
kill $pid
done