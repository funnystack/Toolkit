#!/bin/bash

#应用名
APP_NAME=consul-config

#应用根目录
APP_HOME=/app/

#进程ID
pid=0

cd $APP_HOME

#============================================
# 获取进程ID
#============================================
checkpid() {
   pid=`pgrep ${APP_NAME}`
   if [ -z $pid ]; then
      pid=0
   fi
}

#============================================
# 启动进程
#============================================
start() {
   checkpid
   if [ $pid -ne 0 ]; then
      echo "================================"
      echo "warn: $APP_NAME already started! (pid=$pid)"
      echo "================================"
   else
      echo -n "Starting $APP_NAME ..."
      CMD="python3 /app/heartbeat.py > ${APP_HOME}/${APP_NAME}.log"
      sh -c "$CMD"
      checkpid
      if [ $pid -ne 0 ]; then
         echo "(pid=$pid) [OK]"
         exit 0
      else
         echo "[Failed]"
         ps -ef
         exit 1
      fi
   fi
}

#============================================
# 停止进程
#============================================
stop() {
  checkpid
  if [ $pid -ne 0 ]; then
       sh -c "kill -9 $pid"
       flag=$?
       sleep 3
     if [ $flag -eq 0 ]; then
        echo "[$APP_NAME stop OK]"
         exit 0
     else
        echo "[$APP_NAME stop Failed]"
         exit 1
     fi
  fi
   echo "[$APP_NAME stop ]"
   exit 0
}

#============================================
# 进程状态
#============================================
status() {
   checkpid
   if [ $pid -ne 0 ];  then
      echo "$APP_NAME is running! (pid=$pid)"
   else
      echo "$APP_NAME is not running"
   fi
}

case "$1" in
   'start')
      start
      ;;
   'stop')
     stop
     ;;
   'status')
     status
     ;;
  *)
  echo "Usage: $0 {start|stop|status}"
  exit 1
esac
exit 0