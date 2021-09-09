#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-7
# This is the clustering script in the textLearn project.

import re
import os
wd = os.getcwd()

from time import time
from sklearn.cluster import KMeans

from collections import Counter
from scipy.sparse import vstack
from random import choice

from .IO import dataSaver
from .basic import Flatten, Sparsely

class KmeansClustering:

    @staticmethod
    def SparseFeatureBuilder(init, nKeyWords):
        trainX = [[init.Word2Id[x] for x in v['keyWords'] if x in init.Word2Id] for k, v in init.stat.items()]
        trainX = [[y for y in x if y < nKeyWords] for x in trainX]
        trainX = vstack([Sparsely(x, nKeyWords) for x in trainX])
        return trainX

    @staticmethod
    def Train(trainX, init='k-means++', n_clusters=10, n_init=30, max_iter=1000, random_state = None):

        '''

        :param trainX: the training data
        :param n_clusters: Set the n_cluster here!
        :return:
        '''

        n_samples, n_features = trainX.shape

        '''
        print the basic information about the model
        '''
        print("n_clusters: %d, \t n_samples %d, \t n_features %d"
              % (n_clusters, n_samples, n_features))

        # model
        t0 = time()
        estimator = KMeans(init=init, n_clusters=n_clusters, n_init=n_init, max_iter=max_iter, random_state = random_state)
        model = estimator.fit(trainX)
        print("Training time:", time() - t0)

        return model

    @staticmethod
    def ResultSave(saveFileName, stat, model):
        '''

        :param saveFileName:
        :param result:
        :param customerKeyWordDict:
        :param n_clusters:
        :return: save the files
        :return: save the files
        :return: save the files
        '''
        t0 = time()
        nClusters = model.n_clusters

        key2Label = list(zip(list(stat.keys()), model.labels_))
        result = {}
        for i in range(nClusters):
            clusterName = "cluster_" + str(i)
            Keys = [x[0] for x in key2Label if x[1] == i]
            nTexts = len(Keys)

            keyWordCount = {k: v['keyWords'] for k, v in stat.items()}
            keyWordCount = [keyWordCount[k] for k in Keys]
            keyWordCount = Counter(list(Flatten(keyWordCount)))
            keyWordCount = sorted(keyWordCount.items(), key=lambda item: item[1], reverse=True)[:100]

            result[clusterName] = {
                "textKeys": Keys,
                "nTexts": nTexts,
                "keyWordStat": keyWordCount
            }

            print(i)

        dataSaver(result, wd + "/textLearn/clusterResult/" + saveFileName)
        print("Total time spent for saving the clustering result:", time() - t0)

class KmeansClusteringResultAnalysis:

    def __init__(self, result, stat):

        for K, V in result.items():
            cluster_n = int(re.split('_', K)[1])
            for key in V['textKeys']:
                stat[key]['cluster'] = cluster_n
        self.result = result
        self.stat = stat

    def TopNWordsInClusters(self, N):  # N < 100, copy the content to the spreadSheet
        for k, v in self.result.items():
            print(k, ":", 'n_dialogs:', v['nTexts'])
            for a, b in v['keyWordStat'][:N]:
                print(a, '\t', b)

    def RandomTextInCluster(self, cluster_n):
        k = f'cluster_{cluster_n}'
        return choice(self.result[k]['textKeys'])

    def TextsIncludingKeyWord(self, keyWord):
        return [k for k, v in self.stat.items() if keyWord in v['keyWords']]

    def SaveTextsInCluster(self, fileName):
        for k, v in self.result.items():
            with open(fileName + str(k), 'w', encoding='utf-8') as fp:
                for i in range(30):
                    a = choice(v['textKeys'])
                    fp.write(self.stat[a]['text'])
                    fp.write('\n\n')
                fp.close()
