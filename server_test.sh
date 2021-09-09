export FLASK_APP=server_test.py

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8880 --with-threads &

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8881 --with-threads &

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8882 --with-threads &

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8883 --with-threads &

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8884 --with-threads &



export FLASK_APP=freeChatServer_test.py

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8870 --with-threads &

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8871 --with-threads &

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8872 --with-threads &

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8873 --with-threads &

nohup /data/anaconda3/bin/python3 -m flask run --host=0.0.0.0 --port=8874 --with-threads &
