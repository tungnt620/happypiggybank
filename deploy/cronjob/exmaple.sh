#!/usr/bin/env bash
# Only deploy in one server
if ps -ef | grep -v grep | grep 'python manage.py activate_confession' ; then
 echo "already running"
 exit
fi

cd /data/release/confession && /envs/confession/bin/python manage.py activate_confession >>/var/log/crontab/confession/activate_confession.out 2>&1 &
