#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-7
# This is the KmeansClusteringTrain script in the textLearn project.

import os
wd = os.getcwd()

from textLearn.bin.initializer import initializer
from textLearn.bin.IO import modelSaver
from textLearn.bin.clustering import KmeansClustering

if __name__ == '__main__':
    fileName = "5712"
    init = initializer(fileName)

    #fileName = "5712_10"
    nKeyWords = 10000
    nClusters = 200

    '''
    import os
    wd = os.getcwd()
    
    from textLearn.bin.initializer import initializer
    from textLearn.bin.IO import modelSaver
    from textLearn.bin.clustering import KmeansClustering
    from textLearn.bin.textStat import textStat
    
    
    
    
    
    temp = init.stat
    result = dict()
    for u, v in temp.items():
        keyWord = textStat.keyWordExtract(v)
        result[v] = {'keyWords': keyWord, 
                     'feature':[init.Word2Id[w] for w in keyWord if w in init.Word2Id],
                     'label':[]}
    init.stat = result

    with open('5712_stat.json', 'w') as fp:
        json.dump(result, fp)
    '''
    trainX = KmeansClustering.SparseFeatureBuilder(init, nKeyWords)

    KmeansModel = KmeansClustering.Train(trainX,
                                         n_clusters=nClusters,
                                         n_init=30,
                                         max_iter=500)

    KmeansClustering.ResultSave(saveFileName="KmeansClusterResult_" + fileName + "_5",
                                stat=init.stat,
                                model=KmeansModel)

    modelSaver(KmeansModel, wd + "/textLearn/models/Kmeans/Kmeans_" + fileName + "_5")

    pass
