#!/bin/bash
case $1 in
    "up")
    # 启动uwsgi服务
    uwsgi --socket :8000 --buffer-size 32768 --module TeamWorkMindMap.wsgi &
    ;;
    "down")
        # 关闭uwsgi服务
        uport=8000
        lsof -i :$uport | awk '{print $2}' > tmp
        pid=$(awk 'NR==2{print}' tmp);
        kill -9 $pid
        rm tmp
    ;;
esac