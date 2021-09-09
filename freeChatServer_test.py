import json
import os
import textLearn
import re
from textLearn.bin import mainChatDB
from textLearn.bin.basic import OnlyChinese

from flask import Flask
from flask import request

chatBot = mainChatDB.mainChatDB()

app = Flask(__name__)

specificFreeChatDict = {}
with open("specificFreeChat/specificFreeChat.txt", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        line = re.sub(u"\ufeff|\n", "", line)
        temp = line.split("\t")
        specificFreeChatDict[temp[0]] = temp[1]
        
specificFreeChatRulesList = []
with open("specificFreeChat/specificFreeChatRules.txt", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        line = re.sub(u"\ufeff|\n", "", line)
        temp = line.split("\t")
        specificFreeChatRulesList.append(temp)

specificFreeChatReturnRulesList = []
with open("specificFreeChat/specificFreeChatReturnRules.txt", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        line = re.sub(u"\ufeff|\n", "", line)
        temp = line.split("\t")
        specificFreeChatReturnRulesList.append(temp)

# 用于替换一些关键词
specificFreeChatReplaceRulesList = []
with open("specificFreeChat/specificFreeChatReplaceRules.txt", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        line = re.sub(u"\ufeff|\n", "", line)
        temp = line.split("\t")
        specificFreeChatReplaceRulesList.append(temp)


@app.route('/freeChat/')
def route_freeChat():
    text = request.args.get('text')

    if text in specificFreeChatDict:
        
        ret = specificFreeChatDict[text]
        return ret	

#    text = OnlyChinese(text)
        
    for item in specificFreeChatRulesList:
        
        if re.match(pattern=item[0], string=text):
            return item[1]
          
    ret = chatBot.tempChatCollectFromTuLing_SingleString(text)
    for item in specificFreeChatReturnRulesList:
        
        if re.match(pattern=item[0], string=ret):
            return item[1]

    # 用于替换一些关键字
    for item in specificFreeChatReplaceRulesList:
        if re.search(item[0], ret):
            ret = re.sub(item[0], item[1], ret)

    return ret

# \freeChatStressTest
@app.route('/freeChatStressTest/')
def route_freeChatStressTest():
    text = request.args.get('text')
    if text in specificFreeChatDict:
        ret = specificFreeChatDict[text]
        return ret

    text = OnlyChinese(text)

    for item in specificFreeChatRulesList:

        if re.match(pattern=item[0], string=text):
            return item[1]

    ret = '您好，业务上有什么我可以帮助到您的吗？'

    return ret

# \freeChatStressTest
@app.route('/freeChatEmpty/')
def route_freeChatEmpty():
    text = request.args.get('text')

    return ''



@app.route('/freeChatNoLimit/')
def route_freeChatNoLimit():
    text = request.args.get('text')

    text = OnlyChinese(text)
         
    ret = chatBot.tempChatCollectFromTuLing_SingleString(text)

    return ret

