#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
#os.chdir('C://Users//user//Desktop//aicode-master')
wd = os.getcwd()
import re
import json
from textLearn.bin.initializer import initializer
import user_config#User list

init = initializer("5712")

##User list
bc_list = user_config.user.copy()
bc_list.remove('UP')
None_list = ["AICOOL", "AICOOL3", "AI", "AI3"]#product in , return none


##BC label dict
#25 label
with open(wd + "/textLearn/label/default/labelDict.txt", 'r', encoding='utf-8') as f:
    labelDict = {}
    for lines in f.readlines():
        if lines == '\n':
            break
        lines = re.sub('\\ufeff', '', lines)
        vec = re.split(' |\n', lines)
        labelDict[int(vec[0])] = vec[1]
    f.close()

#12 label and 12跟25的对照
with open(wd + "/textLearn/label/default/newLabelDict.txt", 'r', encoding='utf-8') as f:
    newLabelDict = {}
    old2newLabelMap = {}
    for lines in f.readlines():
        if lines == '\n':
            break
        lines = re.sub('\\ufeff', '', lines)
        vec = re.split(' |\n', lines)
        newLabelDict[int(vec[2])] = vec[3]
        old2newLabelMap[int(vec[0])] = int(vec[2])
    f.close()

##UP label dict
#7 label
labelDict_up = {}
with open(wd + "/textLearn/label/labelDict_up.txt", 'r', encoding='utf-8') as f:
    for lines in f.readlines():
        if lines == '\n':
            break
        lines = re.sub('\\ufeff', '', lines)
        vec = re.split(' |\n', lines)
        labelDict_up[int(vec[0])] = vec[1]
    f.close()

##Dictionary for vectorize
#BC Dictionary
t_iter = 0
bc_dt = dict()
nKeyWords = 8000
for u, v in enumerate(init.Word2Id):
    bc_dt[v] = u
    t_iter += 1
    if t_iter >= nKeyWords:
        break  
    
#UP Dictionary
with open(wd + "/textLearn/data/up_dict.json") as json_file: 
    up_dt = json.load(json_file) 
    
#complain Dictionary    
with open(wd + '/textLearn/data/complain_dict.json') as json_file: 
    complain_dt = json.load(json_file) 
    
##py env - version
with open(wd + "/py_version.txt", 'r', encoding='utf-8') as f:
    for lines in f.readlines():
        if lines == '\n':
            break
        version = re.sub('\\ufeff', '', lines)
    f.close()

