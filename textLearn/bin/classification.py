#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
#os.chdir('C://Users//user//Desktop//aicode-master')
wd = os.getcwd()
import time
import pickle
from jieba import lcut
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from scipy.sparse import vstack
#textlearn
import textLearn.bin.preprocessing_func as pre_up
from textLearn.bin.IO import dataLoader, dataSaver
from textLearn.bin.basic import Flatten, Sparsely
from textLearn.bin.textStat import textStat
from textLearn.bin.patch import GrammarAdjust
#Dict and label dict
import textLearn.wordDict.GetDictandLabelDict as GetDict

class textClassification:
    def __init__(self, init):
        self.Word2Id = init.Word2Id
        self.labelDict = GetDict.labelDict
        self.newLabelDict = GetDict.newLabelDict
        self.old2newLabelMap = GetDict.old2newLabelMap
        self.labelDict_up = GetDict.labelDict_up
        self.complain_dt = GetDict.complain_dt        
        self.up_dt = GetDict.up_dt
        self.bc_dt = GetDict.bc_dt
        self.nKeyWords = GetDict.nKeyWords
        self.version = GetDict.version
        
        
    def predict(self, text, model, product="", user=""):         
        text = pre_up.remove_punctuation(text)
        text = GrammarAdjust(text)
        keyWords = textStat.keyWordExtract(text, 5)        
        if user.upper() in ['UP']:      
            #load model & preprocessing
            classifier = pickle.load(open(wd + "/textLearn/models/LR/UP/LR_model", 'rb'))
            tv = pickle.load(open(wd + "/textLearn/models/preprocessing/tv.pkl", 'rb'))
            maxminscaler = pickle.load(open(wd + "/textLearn/models/preprocessing/maxminscaler.pkl", 'rb'))
            
            #comlain
            complain_sentiment = textStat.text2CompalinSentiment_model(text, 
                                                                       self.complain_dt, 
                                                                       section='UP')
            
            #predict result
            text_train_df = pre_up.get_train(text, 
                                             self.up_dt, 
                                             tv,
                                             maxminscaler)
            #return reuslt
            ret = pre_up.Get_Json_result(classifier, 
                                         self.labelDict_up, 
                                         text_train_df, 
                                         keyWords, 
                                         [3],
                                         complain_sentiment,
                                         control='UP', br_rate=1, cf_rate=1)
        else:  
            complain_sentiment = textStat.text2CompalinSentiment_model(text, 
                                                                       self.complain_dt, 
                                                                       section='BC')#textStat.text2CompalinSentiment(text)            
            if product.upper() in GetDict.None_list:#User['AICOOL', 'AICOOL3', 'AI', 'AI3'] return none
                ret = pre_up.Return_none(complain_sentiment)
            else:
                if keyWords:#有关键字    
                    feature = textStat.text2Feature(text, self.Word2Id)
                    feature = [x for x in feature if x < self.nKeyWords]
                    test_1 = [lcut(text)]
                    test_1 = pre_up.vectorize(test_1, 
                                              self.bc_dt)
                    #BC 25 label
                    if product.upper() == "OLD26":
                        model_OLD26 = pickle.load(open(wd+ '//textLearn//models//LR//LR_5712_5', 'rb'))
                        ret = pre_up.Get_Json_result(model_OLD26, 
                                                     self.labelDict, 
                                                     test_1, 
                                                     keyWords,
                                                     feature,
                                                     complain_sentiment,
                                                     control='BC', br_rate=1, cf_rate=1)                         
                    #BC 12 label
                    elif (product.upper() != "OLD26") & (user in GetDict.bc_list):
                        ret = pre_up.Get_Json_result(model, 
                                                     self.newLabelDict, 
                                                     test_1, 
                                                     keyWords, 
                                                     feature,
                                                     complain_sentiment,
                                                     control='BC', br_rate=25/11, cf_rate=1.6)                                            
                else:
                    ret = pre_up.Return_none(complain_sentiment)
        #return reuslt-->json type
        return ret
    
    def getWeights(self, word, model):
        nKeyWords = model.coef_.shape[1]

        if not self.Word2Id[word] < nKeyWords:
            print(f"{word} 该词语不在关键词列表中")
            return f"{word} 该词语不在关键词列表中"
        else:
            ret = {k: model.coef_[:, self.Word2Id[word]][k-1] for k, v in self.labelDict.items()}
            return ret

    def setWeight(self, word, label, model, weight):
        nKeyWords = model.coef_.shape[1]
        dict_key = list(self.Word2Id.keys())
        dict_value = list(self.Word2Id.values())
        if word not in dict_key:
            dict_copy = self.Word2Id
            dict_copy.setdefault(word, max(dict_value)+1)
            self.Word2Id = dict_copy
            
        if not self.Word2Id[word] < nKeyWords:
            tmp = np.zeros((model.coef_.shape[0], self.Word2Id[word]+1))
            tmp[:, :model.coef_.shape[1]] = model.coef_
            model.coef_ = tmp
            model.coef_[label-1, self.Word2Id[word]] = weight            
            return f"词语 {word} 对第 {label} 类：\"{self.labelDict[label]}\"的贡献值被调整为{weight}，原为0"            
        else:
            originWeight = model.coef_[label-1, self.Word2Id[word]] * 1
            model.coef_[label-1, self.Word2Id[word]] = weight
            print(f"词语 {word} 对第 {label} 类：\"{self.labelDict[label]}\"的贡献值被调整为{weight}，原为{originWeight}")
            return f"词语 {word} 对第 {label} 类：\"{self.labelDict[label]}\"的贡献值被调整为{weight}，原为{originWeight}"

    def modelUpdate(self, text, labels, model, rate=1):

        # Todo
        if not isinstance(labels, list):
            return "labels必须以list格式输入！"

        text = GrammarAdjust(text)
        keyWords = textStat.keyWordExtract(text, 5)

        nClasses, nKeyWords = model.coef_.shape

        if not keyWords:
            print("没有在这句话中检测到关键词，模型没有被更新")
            return "没有在这句话中检测到关键词，模型没有被更新"

        elif labels:
            ret = ''
            y = Sparsely([x-1 for x in labels], nClasses).todense().A[0]
            classPossibility = np.array(self.predict(text, model)['classPossibility'])
            change = (y - classPossibility) * classPossibility * (1-classPossibility) * rate
            for keyWord in keyWords:
                if not self.Word2Id[keyWord] < nKeyWords:
                    print(f"{keyWord} 该词语不在关键词列表中, 模型没有被更改\n")
                    ret += f"{keyWord} 该词语不在关键词列表中, 模型没有被更改\n"
                    continue
                model.coef_[:, self.Word2Id[keyWord]] += change
                print(f"词语 {keyWord} 对 {labels} 类别的权重增加，对其它类别权重减少，变化速率为{rate}\n")
                ret += f"词语 {keyWord} 对 {labels} 类别的权重增加，对其它类别权重减少，变化速率为{rate}\n"
            return ret


class LRClassification:
    @staticmethod
    def OriginDatasetBuilder(init, clusterResultName, cluster2LabelName, keyWord2LabelName):

        cluster2Label = {}
        with open(cluster2LabelName, 'r', encoding='utf-8') as f:
            for lines in f.readlines():
                if lines == '\n':
                    break
                vec = re.split(' ', lines)
                cluster2Label[int(vec[0])] = int(vec[1])
            f.close()

        keyWord2Label = {}
        with open(keyWord2LabelName, 'r', encoding='utf-8') as f:
            for lines in f.readlines():
                if lines == '\n':
                    break
                vec = re.split(' ', lines)
                keyWord2Label[vec[0]] = int(vec[1])
            f.close()

        result = dataLoader(clusterResultName)

        for K, V in result.items():
            cluster_n = int(re.split('_', K)[1])
            if cluster_n in cluster2Label:
                for dialogKey in V['textKeys']:
                    init.stat[dialogKey]['label'].append(cluster2Label[cluster_n])

        dialogLabels = []
        for K, V in init.stat.items():
            if len(V['keyWords']) == 0:
                init.stat[K]['label'].append(0)
            for keyWord in V['keyWords']:
                if keyWord in keyWord2Label:
                    init.stat[K]['label'].append(keyWord2Label[keyWord])
            for label in V['label']:
                if label == 0:
                    continue
                dialogLabels.append((K, label))

        originDataset = [(dialogKey, init.stat[dialogKey]['feature'], label) for dialogKey, label in dialogLabels]

        return originDataset


    @staticmethod
    def SparseFeatureBuilder(originDataset, nKeyWords):
        trainX = [observation[1] for observation in originDataset]
        trainX = [[feature for feature in features if feature < nKeyWords] for features in trainX]
        trainX = vstack([Sparsely(features, nKeyWords) for features in trainX])
        return trainX

    @staticmethod
    def LabelBuilder(originDataset):
        label = [observation[2] for observation in originDataset]
        label = np.array(label)
        return label

    @staticmethod
    def Train(X, y):
        solver = 'saga'

        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            random_state=42,
                                                            stratify=y,
                                                            test_size=0.1)
        train_samples, n_features = X_train.shape
        n_classes = np.unique(y).shape[0]

        print('Dataset TextsWordFeature, train_samples=%i, n_features=%i, n_classes=%i'
              % (train_samples, n_features, n_classes))

        models = {'ovr': {'name': 'One versus Rest', 'iters': [1, 3]},
                  'multinomial': {'name': 'Multinomial', 'iters': [1, 3, 7, 20]}}

        for model in models:
            # Add initial chance-level values for plotting purpose
            accuracies = [1 / n_classes]
            times = [0]
            densities = [1]

            model_params = models[model]

            # Small number of epochs for fast runtime
            for this_max_iter in model_params['iters']:
                print('[model=%s, solver=%s] Number of epochs: %s' %
                      (model_params['name'], solver, this_max_iter))
                lr = LogisticRegression(solver=solver,
                                        multi_class=model,
                                        C=1,
                                        penalty='l1',
                                        fit_intercept=True,
                                        max_iter=this_max_iter,
                                        random_state=4180,
                                        class_weight='balanced'
                                        )
                t1 = time.time()
                lr.fit(X_train, y_train)
                train_time = time.time() - t1

                y_pred = lr.predict(X_test)
                accuracy = np.sum(y_pred == y_test) / y_test.shape[0]
                print(accuracy)
                density = np.mean(lr.coef_ != 0, axis=1) * 100
                accuracies.append(accuracy)
                densities.append(density)
                times.append(train_time)
            models[model]['times'] = times
            models[model]['densities'] = densities
            models[model]['accuracies'] = accuracies
            print('Test accuracy for model %s: %.4f' % (model, accuracies[-1]))
            print('%% non-zero coefficients for model %s, '
                  'per class:\n %s' % (model, densities[-1]))
            print('Run time (%i epochs) for model %s:'
                  '%.2f' % (model_params['iters'][-1], model, times[-1]))

        '''
        fig = plt.figure()
        ax = fig.add_subplot(111)

        for model in models:
            name = models[model]['name']
            times = models[model]['times']
            accuracies = models[model]['accuracies']
            ax.plot(times, accuracies, marker='o',
                    label='Model: %s' % name)
            ax.set_xlabel('Train time (s)')
            ax.set_ylabel('Test accuracy')
        ax.legend()
        fig.suptitle('Multinomial vs One-vs-Rest Logistic L1\n'
                     'Dataset %s' % 'DialogsWordFeature')
        fig.tight_layout()
        fig.subplots_adjust(top=0.85)
        run_time = time.time() - t0
        print('Example run in %.3f s' % run_time)
        plt.show()
        '''

        return lr





