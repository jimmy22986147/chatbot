#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Ziqi on 2018/7/4
# This the mainChatDB script in the ChatDB project

import json
import re
import csv
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


class mainChatDB():

    def __init__(self, DBdir='DB'):

        self.tuLingKeys = ['8b005db5f57556fb96dfd98fbccfab84',
                           '577173e62a2ff6627b62e94d663b449c',
                           'd5b73c4420bc4728b08e85a8a6cabb5b',
                           'e8c190a005adc401867efd1ad2602f70',
                           'fa3747334ed3f1a1520238ffa32ea415',
                           '0f25586d336dc4534dba3d1fe6798524',
                           '2ee6e84a755b4ac2b5b2cc25d992b03a',
                           'fac686fd393f9f3131b3f6b4f807639c',
                           '74ba0496b9c8f783ccca78c7e8921e40',
                           'f2920ce871c744a7a058983847770f22',
                           '50e4507dee64093b0620b9c466d74c8c',
                           '35262f70dfb84253ae3b921bc98cca76',
                           'd6cbd5f8ab498744d73764cbfff43729',
                           '2f53be65e323ec8e8b8ccbf42ee7ddc1',
                           # '1a5abf341652465ba8883bf9ab12b2fb',
                           '879a6cb3afb84dbf4fc84a1df2ab7319',
                           'f30e3b04537946dbade6ff935a73c6c1',
                           'c00282de107144fb940adab994d9ff98',
                           'b4521b4718ed4f3fb5bddf6518b8d564',
                           'd59c41e816154441ace453269ea08dba',
                           '83a4a9c76bc14ab888041f72ff47aa88',
                           ]

        # 7、8的额度较多

        self.tuLingKeyIndex = -1
        self.tuLingKey = self.tuLingKeys[self.tuLingKeyIndex]

        self.DBdir = DBdir

        self.mainChatDB = dataLoader(DBdir + "/mainChatDB.json")

        self.topicType = {}
        with open(DBdir + "/topicType.txt", 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            for line in lines:
                spline = line.split(' ')
                self.topicType[int(spline[0])] = re.sub('\n', '', spline[1])

        self.grammarType = {}
        with open(DBdir + "/grammarType.txt", 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            for line in lines:
                spline = line.split(' ')
                self.grammarType[int(spline[0])] = re.sub('\n', '', spline[1])

    def mainChatDBSave(self):

        dataSaver(self.mainChatDB, self.DBdir + "/mainChatDB.json")


    def tempChatInputLoad(self, tempChatDBdir="/tempChatInput.txt"):
        self.tempChatInput = []
        with open(self.DBdir + tempChatDBdir, 'r', encoding='utf-8') as csvfile:
            csvrows = csv.reader(csvfile, delimiter='\t', quotechar='|')
            for row in csvrows:
                row[0] = re.sub("\\ufeff", '', row[0])
                self.tempChatInput.append([row[0], int(row[1]), int(row[2])])

## PingAn

    # def tempChatCollectFromPingAn_SingleCore(self):
    #
    #     ret = self._tempChatCollectFromPingAn_SingleCore(self.tempChatInput)
    #
    #     for k, v in ret.items():
    #
    #         if k not in self.mainChatDB:
    #             self.mainChatDB[k] = v
    #         else:
    #             self.mainChatDB[k]["topicType"] = v["topicType"]
    #             self.mainChatDB[k]["grammarType"] = v["grammarType"]
    #             if v["reply"][0] not in self.mainChatDB[k]["reply"]:
    #                 self.mainChatDB[k]["reply"].append(v["reply"][0])
    #
    #     return ret
    #
    # def tempChatCollectFromPingAn_MultiCore(self, coreNum):
    #
    #     ret = self._tempChatCollectFromPingAn_MultiCore(self.tempChatInput, coreNum)
    #
    #     for k, v in ret.items():
    #
    #         if k not in self.mainChatDB:
    #             self.mainChatDB[k] = v
    #         else:
    #             if v["reply"][0] not in self.mainChatDB[k]["reply"]:
    #                 self.mainChatDB[k]["reply"].append(v["reply"][0])
    #
    #     return ret
    #
    # @staticmethod
    # def tempChatCollectFromPingAn_SingleString(string):
    #
    #     driver = webdriver.Chrome()
    #     driver.get(
    #         "https://ziker-talk.yun.pingan.com/webim/?"
    #         "channel=WEBIM&authorizerAppid=webim2c83aec44342e0a&"
    #         "eid=d794973a9dba37bc0bc206f014774566&"
    #         "theme=07c5ba")
    #     # assert "ziker-talk" in driver.title
    #
    #     elem_sendText = driver.find_element_by_class_name('foot').\
    #         find_element_by_class_name('inner').\
    #         find_element_by_id('send-textarea')
    #     elem_sendText.send_keys(string)
    #     elem_sendText.send_keys(Keys.RETURN)
    #
    #     time.sleep(1)
    #     elem_warp = driver.find_element_by_class_name('im-message-warp')
    #     elem_lastwarp = elem_warp.find_elements_by_class_name('message-warp')[-1]
    #
    #     ret = re.sub("\*\*.*\*\*", "", elem_lastwarp.text)
    #
    #     driver.close()
    #
    #     return ret
    #
    # @staticmethod
    # def _tempChatCollectFromPingAn_SingleCore(tempChatInput):
    #
    #     ret = {}
    #
    #     for item in tempChatInput:
    #         ret[item[0]] = {"reply": "",
    #                         "topicType": item[1],
    #                         "grammarType": item[2]}
    #
    #     driver = webdriver.Chrome()
    #     driver.get(
    #         "https://ziker-talk.yun.pingan.com/webim/?"
    #         "channel=WEBIM&"
    #         "authorizerAppid=webim2c83aec44342e0a&"
    #         "eid=d794973a9dba37bc0bc206f014774566&"
    #         "theme=07c5ba")
    #     # assert "ziker-talk" in driver.title
    #
    #     for k, v in ret.items():
    #
    #         try:
    #
    #             elem_sendText = driver.find_element_by_class_name('foot'). \
    #                 find_element_by_class_name('inner'). \
    #                 find_element_by_id('send-textarea')
    #             elem_sendText.send_keys(k)
    #             elem_sendText.send_keys(Keys.RETURN)
    #
    #             time.sleep(1)
    #             elem_warp = driver.find_element_by_class_name('im-message-warp')
    #             elem_lastwarp = elem_warp.find_elements_by_class_name('message-warp')[-1]
    #
    #             reply = re.sub("\*\*.*\*\*", "", elem_lastwarp.text)
    #             ret[k]["reply"] = [reply]
    #
    #         except Exception as e:
    #
    #             print(e)
    #             pass
    #
    #     driver.close()
    #
    #     return ret
    #
    # @staticmethod
    # def _tempChatCollectFromPingAn_MultiCore(tempChatInput, coreNum):
    #
    #     pool = ThreadPool(coreNum)
    #     tempChatInputs = chunks(tempChatInput, coreNum)
    #     result = pool.map(mainChatDB._tempChatCollectFromPingAn_SingleCore, tempChatInputs)
    #
    #     pool.close()
    #     pool.join()
    #
    #     ret = result[0]
    #     for item in result[1:]:
    #         ret.update(item)
    #
    #     return ret

## TuLing

    def tempChatCollectFromTuLing_SingleCore(self):

        ret = self._tempChatCollectFromTuLing_SingleCore(self.tempChatInput)

        for k, v in ret.items():

            if k not in self.mainChatDB:
                self.mainChatDB[k] = v
            else:
                self.mainChatDB[k]["topicType"] = v["topicType"]
                self.mainChatDB[k]["grammarType"] = v["grammarType"]
                if v["reply"][0] not in self.mainChatDB[k]["reply"]:
                    self.mainChatDB[k]["reply"].append(v["reply"][0])

        return ret

    def tempChatCollectFromTuLing_MultiCore(self, coreNum):

        ret = self._tempChatCollectFromTuLing_MultiCore(self.tempChatInput, coreNum)

        for k, v in ret.items():

            if k not in self.mainChatDB:
                self.mainChatDB[k] = v
            else:
                if v["reply"][0] not in self.mainChatDB[k]["reply"]:
                    self.mainChatDB[k]["reply"].append(v["reply"][0])

        return ret


    def tempChatCollectFromTuLing_SingleString(self, string):

        if self.tuLingKeyIndex >= self.len(self.tuLingKeys):
            self.tuLingKeyIndex -= self.len(self.tuLingKeys)

        tuLingKey = self.tuLingKeys[self.tuLingKeyIndex]

        ret = '呜...本来想回你点什么的...但是突然忘了自己要说什么...委屈...'

        api = 'http://www.tuling123.com/openapi/api?key=' + tuLingKey + '&info='

        for i in range(20):

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
            ret = requests.get('http://i.itpk.cn/api.php?question=' + string).text

        ret = re.sub('微信机器人', '韦小宝', ret)
        ret = re.sub('图灵机器人', '韦小宝', ret)
        ret = re.sub('文秀', '宝宝', ret)
        ret = re.sub('\[cqname\]', '宝宝', ret)

        print(self.tuLingKeyIndex)

        return ret

    @staticmethod
    def _tempChatCollectFromTuLing_SingleCore(tempChatInput):

        ret = {}

        for item in tempChatInput:
            ret[item[0]] = {"reply": "",
                            "topicType": item[1],
                            "grammarType": item[2]}

        for k, v in ret.items():

            reply = mainChatDB.tempChatCollectFromTuLing_SingleString(k)

            ret[k]["reply"] = [reply]

        return ret

    @staticmethod
    def _tempChatCollectFromTuLing_MultiCore(tempChatInput, coreNum):

        pool = ThreadPool(coreNum)
        tempChatInputs = chunks(tempChatInput, coreNum)
        result = pool.map(mainChatDB._tempChatCollectFromTuLing_SingleCore, tempChatInputs)

        pool.close()
        pool.join()

        ret = result[0]
        for item in result[1:]:
            ret.update(item)

        return ret



if __name__ == '__main__':

    a = mainChatDB()
    a.tempChatInputLoad()

    for i in range(1):
        ret = a.tempChatCollectFromTuLing_MultiCore(1)
        a.tempChatInput = []
        for k, v in ret.items():
            a.tempChatInput.append([v['reply'][0], 0, 0])
        a.mainChatDBSave()

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





