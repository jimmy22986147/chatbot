echo " restarting"
ps -ef |grep gunicorn |grep -v grep |awk '{print $2}'|xargs kill -9

cp /data/aicode/nohup.out /data/bak/$DATE_nohup.out
echo >/data/aicode/nohup.out 

source /data/thispy/bin/activate
GUNICORN=$(which gunicorn)
nohup $GUNICORN -b 0.0.0.0:8881 server_test:app -c gunicorn.conf.py &
nohup $GUNICORN -b 0.0.0.0:8882 freeChatServer_test:app -c gunicorn.conf.py &

echo "完成"

