#!/bin/bash
# 获取当前时间
current_time=$(date '+%Y-%m-%d %H:%M:%S')
# 输出当前时间，并追加到文件
echo "$current_time" >> /app/time.log

/usr/local/bin/python3 /app/consul_config_backup.py