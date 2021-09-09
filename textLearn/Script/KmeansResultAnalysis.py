#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by ziqi on 18/1/18
# This the KmeansResultAnalysis script in the textLearn project.

import re
import os
wd = os.getcwd()

from textLearn.bin.initializer import initializer
from textLearn.bin.IO import dataLoader
from textLearn.bin.clustering import KmeansClusteringResultAnalysis

import jieba.analyse
jieba.load_userdict(wd + "/textLearn/wordDict/userDict")
jieba.analyse.set_stop_words(wd + "/textLearn/wordDict/stopDict")
userDict = []
with open(wd + "/textLearn/wordDict/userDict", 'r', encoding='utf-8') as f:
    for lines in f.readlines():
        vec = re.split(' ', lines)
        userDict.append(vec[0])
    f.close()



if __name__ == '__main__':

    fileName = "5712"
    nKeyWords = 10000
    nClusters = 200

    init = initializer(fileName)
    stat = init.stat
    result = dataLoader(wd + "/textLearn/clusterResult/KmeansClusterResult_5712_4")
    KmeansRA = KmeansClusteringResultAnalysis(result, stat)

    KmeansRA.TopNWordsInClusters(10)  # print topN key words for each cluster
    print(len(KmeansRA.TextsIncludingKeyWord(u'反水')))  # find the text keys which include the target key word
    KmeansRA.RandomTextInCluster(8)  #
    KmeansRA.SaveTextsInCluster(wd + "/textLearn/clusterResult/textsInCluster/")
