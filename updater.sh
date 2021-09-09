branch=jimmy_temp
# source /data/thispy/bin/activate
# GUNICORN=$(which gunicorn)

echo 'updating...'
git update-index --assume-unchanged updater.sh
git update-index --assume-unchanged user_config.py
sudo git add .
#DATE=$(date +%Y%m%d)

sudo git commit -m $DATE' auto updated'
sudo git pull origin $branch
sudo git push origin $branch


# echo 'restarting...'
# sudo ps -ef |grep gunicorn |grep -v grep |awk '{print $2}'|xargs kill -9

# sudo nohup $GUNICORN -b 0.0.0.0:8881 server_test:app -c gunicorn.conf.py &
# sudo nohup $GUNICORN -b 0.0.0.0:8882 freeChatServer_test:app -c gunicorn.conf.py &

echo 'finished'