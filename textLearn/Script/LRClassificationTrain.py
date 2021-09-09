#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-9
# This is the LRClassificationTrain script in the textLearn project.

import os
#os.chdir('C://Users//user//Desktop//aicode-master')
wd = os.getcwd()

from textLearn.bin.initializer import initializer
from textLearn.bin.IO import modelSaver, dataSaver
from textLearn.bin.classification import LRClassification

if __name__ == '__main__':

    cluster2LabelName = wd + "/textLearn/label/cluster2Label_5.txt"
    keyWord2LabelName = wd + "/textLearn/label/keyWord2Label_5.txt"
    labelDictName = wd + "/textLearn/label/labelDict_5.txt"
    clusterResultName = wd + "/textLearn/clusterResult/KmeansClusterResult_5712_5"
    fileName = "5712"
    nKeyWords = 8000

    init = initializer(fileName)

    originDataset = LRClassification.OriginDatasetBuilder(init, 
                                                          clusterResultName, 
                                                          cluster2LabelName, 
                                                          keyWord2LabelName)

    trainX = LRClassification.SparseFeatureBuilder(originDataset, nKeyWords)
    trainY = LRClassification.LabelBuilder(originDataset)
    LRModel = LRClassification.Train(trainX, trainY)

    modelSaver(LRModel, wd + "/textLearn/models/LR/LR_" + fileName + "_6")

    lrAttr = {
        'cluster2LabelName': cluster2LabelName,
        'keyWord2LabelName': keyWord2LabelName,
        'labelDictName': labelDictName,
        'clusterResultName': clusterResultName,
        'fileName': fileName,
        'nKeyWords': nKeyWords
    }
    dataSaver(lrAttr, wd + "/textLearn/models/LR/LRAttr_" + fileName + "_6")

    pass
