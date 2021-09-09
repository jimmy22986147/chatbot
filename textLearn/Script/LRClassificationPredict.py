#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-9
# This is the LRClassificationPredict script in the textLearn project.
import os
wd = os.getcwd()
from textLearn.bin.initializer import initializer
from textLearn.bin.classification import textClassification
from textLearn.bin.IO import modelLoader, modelSaver

if __name__ == '__main__':

    init = initializer("5712")
    #labelDictPath = wd + "/textLearn/label/labelDict_5.txt"
    LRModel = modelLoader(wd + "/textLearn/models/LR/LR_5712_5")

    tc = textClassification(init)
    # print(tc.predict("你好,请帮我刷新一下流水", LRModel))
    # tc.predict("账号冻结&amp;nbsp;&amp;nbsp", LRModel)
    # tc.predict("自助体验金领取提示安全级别不够是怎么回事啊？", LRModel)


    ret = tc.predict("为什么我的存款还没到账？", LRModel)
    for k in ['classConfident','label','labelMeaning']:
        print (k, ":", ret[k])

    #print("\"到帐\"这个词对第一类的权重： ", tc.getWeights('到帐', LRModel)[0])
    tc.setWeight('pt', 1, LRModel, weight=2.21)
    tc.setWeight('aaa', 1, LRModel, weight=2.21)

    pass
