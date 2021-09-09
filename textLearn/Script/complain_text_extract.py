#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 19-8-11
# This is the complain_text_extract script in the textLearn_1.0.1_deploy project.

import json
import jieba
from textLearn import tc

import textLearn
import os
import re

wd = os.getcwd()
dirtyWordDict = []
with open(wd + "/textLearn/wordDict/dirtyWordDict.txt", 'r', encoding='utf-8') as f:
    for lines in f.readlines():
        vec = re.split(' ', lines)
        dirtyWordDict.append(vec[0])
    f.close()
dirtyWordDict = set(dirtyWordDict)

def ifDirty(text):

    def dirtyWordExtract(text):
        DD = [x for x in jieba.cut(text, cut_all=True) if x in dirtyWordDict]  #dirtyWordDict
        return list(set(DD))

    return bool(dirtyWordExtract(text))


product_list = os.listdir('textLearn/data/AI_speech')

dirty_text = []

for product in product_list:
    file_list = os.listdir('textLearn/data/AI_speech/' + product)
    for file in file_list:

        with open('textLearn/data/AI_speech/' + product + '/' + file, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            for item in data:
                for speech in item['dialog']:
                    if speech['speaker'] == 'customer':
                        print(speech['text'])
                        if ifDirty(speech['text']):
                            dirty_text.append(speech['text'])



with open('complains.csv', 'w', encoding='utf-8') as fp:
    for text in dirty_text:
        fp.write(text)
        fp.write('\n')
    fp.close()


if __name__ == '__main__':
    pass