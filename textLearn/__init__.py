#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-12
# This is the __init__ script in the textLearn project.
from user_config import user
import os
wd = os.getcwd()

from textLearn.bin.initializer import initializer
from textLearn.bin.classification import textClassification
from textLearn.bin.IO import modelLoader, modelSaver


init = initializer("5712")
LRModel = {}
for u in user:
    LRModel[u] = modelLoader(wd + "/textLearn/models/LR/" + u + "/LR_model")

tc = textClassification(init)
#chatbot.Chat_Bot('你好')
