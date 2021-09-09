#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Ziqi on 2018/7/4
# This the mainChatDB script in the ChatDB project

import json
import re
import csv
import urllib
from urllib.parse import quote
from urllib.request import urlopen
import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import sys
import time
from multiprocessing.dummy import Pool as ThreadPool
from textLearn.bin.IO import dataLoader, dataSaver
from textLearn.bin.basic import chunks
from functools import lru_cache


class mainChatDB():

    def __init__(self):

        self.tuLingKeys = [
           # '8b005db5f57556fb96dfd98fbccfab84',
           # '577173e62a2ff6627b62e94d663b449c',
           # 'd5b73c4420bc4728b08e85a8a6cabb5b',
           # 'e8c190a005adc401867efd1ad2602f70',
           # 'fa3747334ed3f1a1520238ffa32ea415',
           # '0f25586d336dc4534dba3d1fe6798524',
           # '2ee6e84a755b4ac2b5b2cc25d992b03a',
           # 'fac686fd393f9f3131b3f6b4f807639c',
           # '74ba0496b9c8f783ccca78c7e8921e40',
           # 'f2920ce871c744a7a058983847770f22',
           # '50e4507dee64093b0620b9c466d74c8c',
           # '35262f70dfb84253ae3b921bc98cca76',
           # 'd6cbd5f8ab498744d73764cbfff43729',
           '2f53be65e323ec8e8b8ccbf42ee7ddc1',
           # '1a5abf341652465ba8883bf9ab12b2fb',
           # '879a6cb3afb84dbf4fc84a1df2ab7319',
           # 'f30e3b04537946dbade6ff935a73c6c1',
           'c00282de107144fb940adab994d9ff98',
           # 'b4521b4718ed4f3fb5bddf6518b8d564',
           # 'd59c41e816154441ace453269ea08dba',
           # '83a4a9c76bc14ab888041f72ff47aa88',
                           ]

        # 7、8的额度较多

        self.tuLingKeyIndex = -1
        self.tuLingKey = self.tuLingKeys[self.tuLingKeyIndex]

    @lru_cache(250)
    def tempChatCollectFromTuLing_SingleString(self, string):
        sess = requests.get('https://api.ownthink.com/bot?spoken='+string)
        ret = sess.text
        answer = json.loads(ret)['data']['info']['text']
        return answer
        # 优先调用青云客的接口
        #ret = qingyunke(string)
        #if ret:
        #    return ret

        if self.tuLingKeyIndex >= len(self.tuLingKeys):
            self.tuLingKeyIndex -= len(self.tuLingKeys)

        tuLingKey = self.tuLingKeys[self.tuLingKeyIndex]

        ret = '呜...本来想回你点什么的...但是突然忘了自己要说什么...委屈...'

        api = 'http://www.tuling123.com/openapi/api?key=' + tuLingKey + '&info='

        for i in range(len(self.tuLingKeys)):

            try:
                result_json = requests.get(api + string).json()
                ret = result_json['text']
                print(ret)

            except Exception as e:
                print(e)
                ret = '呜...本来想回你点什么的...但是突然忘了自己要说什么...委屈...'
                return ret

            if re.match('亲爱的，当天请求次数已用完', ret):
                self.tuLingKeyIndex += 1
                if self.tuLingKeyIndex >= len(self.tuLingKeys):
                    self.tuLingKeyIndex -= len(self.tuLingKeys)
                tuLingKey = self.tuLingKeys[self.tuLingKeyIndex]
                api = 'http://www.tuling123.com/openapi/api?key=' + tuLingKey + '&info='

            else:
                break

        if re.match('亲爱的，当天请求次数已用完', ret):
            try:
                ret = json.loads(requests.get('http://i.itpk.cn/api.php?question=' + string).text.replace('\ufeff', ''))
                ret = ret['content']
            except Exception as err:
                ret = requests.get('http://i.itpk.cn/api.php?question=' + string).text

        ret = re.sub('微信机器人', '韦小宝', ret)
        ret = re.sub('图灵机器人', '韦小宝', ret)
        ret = re.sub('文秀', '宝宝', ret)
        ret = re.sub('\[cqname\]', '宝宝', ret)
        ret = re.sub('\[name\]', '你', ret)
        ret = re.sub('\[zodiac\]', '金牛座', ret)

        ret = re.sub('智商', '心情', ret)
        ret = re.sub('恶心', '欺负人', ret)
        ret = re.sub('就算了', '好难过', ret)
        ret = re.sub('变卖公司财产', '努力赚钱', ret)

        if ("http" in ret) or ("360" in ret):
            ret = "你想说什么呢？"

        # print(self.tuLingKeyIndex)

        return ret

def qingyunke(msg):
    """
    智能聊天接口
    :param msg:
    :return:
    """
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
    html = requests.get(url)
    return html.json()["content"]


if __name__ == '__main__':

    a = mainChatDB()

    pass

#  青云客
#  r = requests.post('http://api.qingyunke.com/api.php?key=free&appid=0&msg=怎么回事').json()
# n = 0
# import requests
# import re
# string = '你好啊'
# for tuLingKey in tuLingKeys:
#     r = requests.post('http://www.tuling123.com/openapi/api?key=' + tuLingKey + '&info=' + string)
#     r1 = requests.get('http://i.itpk.cn/api.php?question=' + string).text
#     r1 = re.sub('\[cqname\]', '宝宝', r1)
#     print(r.json())
#     print(r1)
#     print(n)
#     n += 1





