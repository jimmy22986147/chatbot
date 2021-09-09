echo 'starting...'
time=$(date +%Y-%m-%d)
logs="/tmp/aicode/logs/aipy-${time}.log"
/usr/local/bin/virtualenv -p python3.6 thispy
nohup /usr/local/bin/gunicorn -b 0.0.0.0 /tmp/aicode/server_test:app -c /tmp/aicode/gunicorn.conf.py >> $logs &