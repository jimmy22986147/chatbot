import re
import os
wd = os.getcwd()
import pandas as pd
import numpy as np
from collections import Counter
from textLearn.bin.basic import Flatten, OnlyGoodString
from textLearn.bin.IO import dataLoader, dataSaver
import string
import jieba.analyse
from jieba import lcut
import textLearn.bin.preprocessing_func as pre_up
import pickle

jieba.load_userdict(wd + "/textLearn/wordDict/userDict")
jieba.analyse.set_stop_words(wd + "/textLearn/wordDict/stopDict")

userDict = []
with open(wd + "/textLearn/wordDict/userDict", 'r', encoding='utf-8') as f:
    for lines in f.readlines():
        vec = re.split(' ', lines)
        userDict.append(vec[0])
    f.close()
userDict = set(userDict)

dirtyWordDict = {}
with open(wd + "/textLearn/wordDict/dirtyWordDict.txt", 'r', encoding='utf-8-sig') as f:
    for lines in f.readlines():
        vec = re.split(' ', lines)
        dirtyWordDict[vec[0]] = {
            'count': int(vec[1]),
            'complain_degree': int(vec[2]),
            'losing_money': int(vec[3]),
            'urging': int(vec[4]),
        }
    f.close()

class textStat:

    def __init__(self, text, Word2Id):

        self.text = text
        # self.wordCut = self.wordCut(text)
        self.keyWords = self.keyWordExtract(text)
        self.feature = self.statFeature(Word2Id)
        self.intention = self.text2Intention(text)
        self.entity = self.text2Entity(text)
        self.sentiment = self.text2Sentiment(text)
        self.cluster = []
        self.label = []


    def statFeature(self, Word2Id):
        # first we need to get a wc(word count) file
        feature = [Word2Id[w] for w in self.keyWords if w in Word2Id]
        return feature

    @staticmethod
    def wordCut(text):
        return(jieba.lcut(text, cut_all=True))

    @staticmethod
    def keyWordExtract(text, topK=5):
        keyWordListTR = jieba.analyse.textrank(text, topK=topK)  #textRank
        keyWordListTI = jieba.analyse.extract_tags(text, topK=topK)  #TFIDF
        keyWordListUD = [x for x in jieba.cut(text, cut_all=True) if x in userDict]  #userDefine
        return list(set(keyWordListTR + keyWordListTI + keyWordListUD))
    
    @staticmethod
    def dirtyWordExtract(text):
        DD = {x: dirtyWordDict[x] for x in jieba.cut(text, cut_all=True) if x in dirtyWordDict}  #dirtyWordDict
        return DD

    @staticmethod
    def text2Feature(text, Word2Id):
        # first we need to get a wc(word count) file
        keyWords = textStat.keyWordExtract(text)
        feature = [Word2Id[w] for w in keyWords if w in Word2Id]
        return feature

    @staticmethod
    def text2Intention(text):

        #todo: text2Intention

        return []

    @staticmethod
    def text2Entity(text):

        #todo: text2Entity

        return[]

    @staticmethod
    def text2Sentiment(text):

        #todo: text2Sentiment

        return[]

    @staticmethod
    def text2CompalinSentiment(text):
        dirtyWords = textStat.dirtyWordExtract(text)
        complain_degree = sum([v['complain_degree'] for k, v in dirtyWords.items()])
        losing_money = sum([v['losing_money'] for k, v in dirtyWords.items()])
        urging = sum([v['urging'] for k, v in dirtyWords.items()])
        ret = {
            'complain': bool(dirtyWords),
            'normal_complain': (complain_degree == 1),
            'serious_complain': (complain_degree > 1),
            'losing_money': (losing_money > 0),
            'urging': (urging > 0),
        }
        return ret

    @staticmethod
    def text2CompalinSentiment_model(text, dt, section='BC'):
        #严重抱怨> 一般抱怨 > 输钱 > 催促
        if section == 'BC':
            change_dict = {'一般抱怨':0, '严重抱怨':1, '催促':2, '输钱':3, '非抱怨':4}
            complain_model = pickle.load(open(wd + "/textLearn/models/Complain/bc_complain_model", 'rb'))
            complain_tv = pickle.load(open(wd + "/textLearn/models/Complain/tv_bc_complain.pkl", 'rb'))
            complain_maxminscaler = pickle.load(open(wd + "/textLearn/models/Complain/maxminscaler_bc_complain.pkl", 'rb'))
        elif section == 'UP':
            #change_dict = {'一般抱怨':0, '严重抱怨':1, '催促':2, '非抱怨':3}
            #complain_model = pickle.load(open(wd + "/textLearn/models/Complain/complain_model", 'rb'))
            #complain_tv = pickle.load(open(wd + "/textLearn/models/Complain/tv_up_complain.pkl", 'rb'))
            #complain_maxminscaler = pickle.load(open(wd + "/textLearn/models/Complain/maxminscaler_up_complain.pkl", 'rb'))
            change_dict = {'一般抱怨':0, '严重抱怨':1, '催促':2, '0':3, '非抱怨':4}
            complain_model = pickle.load(open(wd + "/textLearn/models/Complain/bc_complain_model", 'rb'))
            complain_tv = pickle.load(open(wd + "/textLearn/models/Complain/tv_bc_complain.pkl", 'rb'))
            complain_maxminscaler = pickle.load(open(wd + "/textLearn/models/Complain/maxminscaler_bc_complain.pkl", 'rb'))
            
        change_dict_verse = {v: k for k, v in change_dict.items()}        
        text_train_df = pre_up.get_train(text, 
                                         dt, 
                                         complain_tv,
                                         complain_maxminscaler)        

        y = complain_model.predict(text_train_df)
        result = change_dict_verse[y[0]]
        
        ret = {
            'complain': result in ['一般抱怨', '严重抱怨', '催促', '输钱'],
            'normal_complain': (result == '一般抱怨'),
            'serious_complain': (result == '严重抱怨'),
            'losing_money': (result == '输钱'),
            'urging': (result == '催促'),
        }
        return ret


def keyWordStat(data, sort = True):
    keyWordList = list(Flatten([textStat.keyWordExtract(OnlyGoodString(v['text'])) for k, v in data.items()]))
    keyWordCount = Counter(keyWordList)
    if not sort:
        return keyWordCount
    return sorted(keyWordCount.items(), key=lambda item: item[1], reverse=True)
