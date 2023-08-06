#!/bin/sh

# start-stop-daemon --stop --signal 1 --quiet --pidfile /var/run/v2ray.pid

# PIDFILE=/var/run/v2ray.pid
# DAEMON=/usr/bin/v2ray
# LOGFILE=/data/91porn/logs/v2ray.log
# CFGFILE=/etc/v2ray/config.json

PIDFILE="$4"
DAEMON="`pwd`/$2"
LOGFILE="`pwd`/v2ray.log"
# CFGFILE="`pwd`/$3"
CFGFILE="$3"

do_start()  
{
  if [ ! -e $CFGFILE ];then
    echo "$CFGFILE not found" >> $LOGFILE 2>&1
    return 5
  fi
  start-stop-daemon --start  --pidfile $PIDFILE --exec $DAEMON --test >> $LOGFILE 2>&1  || return 1
  start-stop-daemon --start  --pidfile $PIDFILE --exec $DAEMON --background -m -- -config $CFGFILE >> $LOGFILE 2>&1 || return 2
}


do_stop()  
{
  # pid=`pidof $DAEMON`
  # if [ -e $PIDFILE ];then
  #     if [ $((${#pid})) -gt 0 ];then
  #         if [ "`cat $PIDFILE`" -eq "$pid" ];then
  #             start-stop-daemon --stop --quiet --retry=TERM/30/KILL/5 --pidfile $PIDFILE
  #         fi
  #     fi
  # fi
  if [ -e $PIDFILE ];then
    start-stop-daemon --stop --quiet --retry=TERM/30/KILL/5 --pidfile $PIDFILE
  fi
}

do_reload()
{
    do_stop || return 3
    do_start || return 4
}

case "$1" in  
  start)
    do_start
  ;;
  stop)
    do_stop
  ;;
  status)
    pidof v2ray >&2
  ;;
  reload)
    do_reload
  ;;
  *)
    #echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload}" >&2
    echo "Usage: v2ray {start|stop|status|reload}" >&2
    exit 3
    ;;
esac