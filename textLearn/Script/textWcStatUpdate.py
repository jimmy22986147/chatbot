#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-7
# This is the textWcStatUpdate script in the textLearn project.


from textLearn.bin.initializer import initializer
from textLearn.bin.IO import dataSaver
from textLearn.bin.textStat import textStat, keyWordStat
from time import time

if __name__ == '__main__':
    t = time()
    fileName = "5712"

    init = initializer(fileName)

    wc = keyWordStat(init.textData, sort=True)
    dataSaver(wc, init.wcFileName)
    print(f"The wc file for {fileName} has been successfully saved! There are totally {len(wc)} words")

    Id2Word = {a: b[0] for a, b in enumerate(wc)}
    Word2Id = {v: k for (k, v) in Id2Word.items()}
    stat = {k: textStat(v['text'], Word2Id).__dict__ for k, v in init.textData.items()}
    dataSaver(stat, init.statFileName)
    print(f"The stat file for {fileName} has been successfully saved! Totally {len(stat)} texts have been handled.")
    print(f"The total time spent is {time()-t}s")
