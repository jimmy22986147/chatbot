import requests
import time
from threading import Thread

a = []
def test():
    t = time.time()
    for i in range(200):
        ret = requests.get('http://localhost:8881/freeChatStressTest/你好啊')
    t_total = time.time() - t
    a.append(t_total)
    
for i in range(100):
    Thread(target=test, args=()).start()
    
a.sort(reverse=True)
print(a)
