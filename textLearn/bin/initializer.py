#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-7
# This is the initializer script in the textLearn project.

import os
from time import time
from os.path import isfile

from textLearn.bin.IO import dataSaver, dataLoader


class initializer:

    def __init__(self, fileName):

        t = time()

        wd = os.getcwd()

        textFileName = wd + "/textLearn/data/" + fileName + "_text.json"
        wcFileName = wd + "/textLearn/wc/" + fileName + "_wc.json"
        statFileName = wd + "/textLearn/data/" + fileName + "_stat.json"

        if isfile(textFileName):
            textData = dataLoader(textFileName)
        else:
            textData = None
            print("No origin textData file in the \'textLearn/data/\' direcotory, initialization for classifier only")

        if isfile(wcFileName):
            wc = dataLoader(wcFileName)
            Id2Word = {a: b[0] for a, b in enumerate(wc)}
            Word2Id = {v: k for (k, v) in Id2Word.items()}
        else:
            wc = None
            Id2Word = None
            Word2Id = None

        if isfile(statFileName):
            stat = dataLoader(statFileName)
        else:
            stat = None

        self.textFileName = textFileName
        self.wcFileName = wcFileName
        self.statFileName = statFileName
        self.textData = textData
        self.wc = wc
        self.stat = stat
        self.Id2Word = Id2Word
        self.Word2Id = Word2Id
        print(f"Initialization finished! The total time spent is {round(time() - t,2)}s")

