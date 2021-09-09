#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
#os.chdir('C://Users//user//Desktop//aicode-master')
wd = os.getcwd()
sys.path.append(wd)
sys.path.append(wd+ '//Unionfunc//ConnectMySQL')
sys.path.append(wd+ '//textLearn//updatemodel')
import ConnectMySQL as ConnectMySQL
import pickle
from datetime import datetime
import numpy as np
import string
import re
import pandas as pd
from jieba import lcut
import textLearn
from textLearn.bin.initializer import initializer
from textLearn import tc
import time
from scipy.sparse import csr_matrix
#sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import logging
import json
import updatemodel_preprocessingfunc as preprocessingfunc
from sklearn.preprocessing import MinMaxScaler
logging.basicConfig(filename='logging.log', 
                    level=logging.INFO)      

def main(ip, user, passw):
    #variable zone
    #sql connect    
    sqlconnect = ConnectMySQL.MySqlConnect(ip, user, passw)#('203.86.236.69', 'jimmyai', 'DADgDaijiMmY46hE*&GT')
    #time
    now_str = datetime.now().strftime('%Y%m')
    #now_str = '202103'
    now_str_datetime = datetime.now().strftime('%Y/%m/%d')
    
    #dictionary-bc
    t_iter = 0
    nKeyWords = 8000
    dt = dict()
    for u, v in enumerate(textLearn.init.Word2Id):
        dt[v] = u
        t_iter += 1
        if t_iter >= nKeyWords:
            break
    #dictionary-up
    with open(wd + "/textLearn/data/up_dict.json") as json_file: 
        up_dt = json.load(json_file) 
    
    
        
    
    labelDict_up = {}
    with open(wd + "/textLearn/label/labelDict_up.txt", 'r', encoding='utf-8') as f:
        for lines in f.readlines():
            if lines == '\n':
                break
            lines = re.sub('\\ufeff', '', lines)
            vec = re.split(' |\n', lines)
            labelDict_up[int(vec[0])] = vec[1]
        f.close()    
    
    #train the model
    #Read wrong info and insert the data to db and update status
    try:
        if ip ==  '203.86.236.69':
            data_for_wrong_bc, before_data_bc, recent_data_bc = preprocessingfunc.Getwrongdata(sqlconnect, 
                                                                                               now_str, 
                                                                                               now_str_datetime,
                                                                                               'BC', 
                                                                                               control='prod')
            data_for_wrong_up, before_data_up, recent_data_up = preprocessingfunc.Getwrongdata(sqlconnect, 
                                                                                               now_str,
                                                                                               now_str_datetime,
                                                                                               'UP',
                                                                                               control='prod')    
        else:
            sys.exit()
    except Exception as e:
        logging.error(e)
        
    #Read before data
    if (data_for_wrong_bc.empty) & (data_for_wrong_up.empty):
        sys.exit()
    
    if data_for_wrong_bc.shape[0] > 0:
        before_data_bc = preprocessingfunc.Random_choice_sample(before_data_bc, 80000)
        update_list = data_for_wrong_bc[['USER', 'PRODUCT']].drop_duplicates()       
        for j in range(len(update_list)):
            user_iter , product_iter = update_list.USER[j], update_list.PRODUCT[j]
            if product_iter.upper() in ["AICOOL", "AICOOL3", "AI", "AI3"]:
                continue
            elif product_iter.upper() in ["OLD26"]:
                recent_data_bc_iter = recent_data_bc[(recent_data_bc.USER == user_iter) & (recent_data_bc.PRODUCT == product_iter)]
                recent_data_bc_iter = recent_data_bc_iter[['DIALOGUE_CONTENT', 'QUESTION_TYPE']].reset_index(drop=True)
                recent_data_bc_iter = preprocessingfunc.Random_choice_sample(recent_data_bc_iter, 10000)
                
                before_data_bc_iter = preprocessingfunc.train_12or26(before_data_bc, 
                                                                     tc.labelDict,
                                                                     tc.old2newLabelMap, 
                                                                     tc.newLabelDict, 
                                                                     form='OldStr_OldEncoding')
                recent_data_bc_iter = preprocessingfunc.train_12or26(recent_data_bc_iter, 
                                                                     tc.labelDict, 
                                                                     tc.old2newLabelMap, 
                                                                     tc.newLabelDict, 
                                                                     form='OldStr_OldEncoding')            
                data = pd.concat([before_data_bc_iter, recent_data_bc_iter], axis=0)
                del(before_data_bc_iter, recent_data_bc_iter)
            else:
                recent_data_bc_iter = recent_data_bc[(recent_data_bc.USER == user_iter) & (recent_data_bc.PRODUCT == product_iter)]
                recent_data_bc_iter = recent_data_bc_iter[['DIALOGUE_CONTENT', 'QUESTION_TYPE']].reset_index(drop=True)
                recent_data_bc_iter = preprocessingfunc.Random_choice_sample(recent_data_bc_iter, 10000)
                
                before_data_bc_iter = preprocessingfunc.train_12or26(before_data_bc, 
                                                                     tc.labelDict,
                                                                     tc.old2newLabelMap, 
                                                                     tc.newLabelDict, 
                                                                     form='OldStr_NewEncoding')
                recent_data_bc_iter = preprocessingfunc.train_12or26(recent_data_bc_iter, 
                                                                     tc.labelDict, 
                                                                     tc.old2newLabelMap, 
                                                                     tc.newLabelDict, 
                                                                     form='NewStr_NewEncoding')            
                data = pd.concat([before_data_bc_iter, recent_data_bc_iter], axis=0)
                del(before_data_bc_iter, recent_data_bc_iter)   
                         
            train_list_vec = [lcut(text) for text in data.DIALOGUE_CONTENT]            
            train_list_vec = preprocessingfunc.vectorize(train_list_vec, dt)
            maxminscaler = MinMaxScaler()
            maxminscaler.fit(train_list_vec)
            train_list_vec = maxminscaler.transform(train_list_vec)
            train_x, test_x ,train_y, test_y= train_test_split(csr_matrix((train_list_vec), dtype=float),
                                                               data.label,
                                                               test_size=0.2, 
                                                               random_state=1234)
            del(train_list_vec, data)
            lr = LogisticRegression(solver='saga',
                                    multi_class='multinomial',
                                    C=1,
                                    penalty='l1',
                                    fit_intercept=True,
                                    max_iter=5000,
                                    random_state=4180,
                                    class_weight='balanced')#,n_jobs=16)
                                    
            lr.fit(train_x, train_y)
            accuracy = lr.score(test_x, test_y)
            accuracy
            if accuracy >= 0.8:
                filename = wd+ '//textLearn//models//LR//'+user_iter+ '//LR_model'
                pickle.dump(lr, open(filename, 'wb'))  
            else:
                logging.info('{time}_{user}_{product}-模型沒超過80%，所以沒更新'.format(time=now_str_datetime,
                                                                                       user=user_iter,
                                                                                       product=product_iter))
    
    if data_for_wrong_up.shape[0] > 0:
        #feature engineering function
        tv = pickle.load(open(wd + "/textLearn/models/nb/tv.pkl", 'rb')) 
        #before
        before_data_up = preprocessingfunc.Random_choice_sample(before_data_up, 40000)    
        recent_data_up = preprocessingfunc.Random_choice_sample(recent_data_up, 10000)
        #recent
        data = pd.concat([before_data_up[['DIALOGUE_CONTENT', 'QUESTION_TYPE']], 
                          recent_data_up[['DIALOGUE_CONTENT', 'QUESTION_TYPE']]], axis=0)
        del(before_data_up, before_data_up)     
        data.loc[:, 'DIALOGUE_CONTENT'] = data.loc[:, 'DIALOGUE_CONTENT'].apply(preprocessingfunc.remove_punctuation)
        
        train_list = [lcut(text) for text in data.DIALOGUE_CONTENT]
        train_list_vec = preprocessingfunc.vectorize(train_list, up_dt)    
        
        data['char_count'] = data['DIALOGUE_CONTENT'].apply(len)
        data['word_count'] = data['DIALOGUE_CONTENT'].apply(lambda x: len(x.split()))
        data['word_density'] = data['char_count'] / (data['word_count']+1)
        data['punctuation_count'] = data['DIALOGUE_CONTENT'].apply(lambda x: len("".join(_ for _ in x if _ in string.punctuation)))
        
        
        add_feature_ = data[['word_count', 'word_density', 'punctuation_count']].values
        add_feature_isin = np.array([preprocessingfunc.add_feature(i) for i in data.DIALOGUE_CONTENT])
        tv_fit = tv.transform(data.DIALOGUE_CONTENT)
        
        train_data = np.c_[np.array(train_list_vec), add_feature_isin, tv_fit.toarray(), add_feature_]
        label_change = [labelDict_up[i] for i in data.QUESTION_TYPE]
        data.loc[:, 'label'] = label_change
        
        train_x, test_x ,train_y, test_y= train_test_split(csr_matrix((train_data), dtype=float),
                                                           data.label,
                                                           test_size=0.2, 
                                                           random_state=1234)
        del(train_data, data)
        lr = LogisticRegression(solver='saga',
                                multi_class='multinomial',
                                C=1,
                                penalty='l1',
                                fit_intercept=True,
                                max_iter=5000,
                                random_state=1234,
                                class_weight='balanced')#,n_jobs=16)
                                
        lr.fit(train_x, train_y)
        accuracy = lr.score(test_x, test_y)
        
        if accuracy >= 0.8:
            filename = wd+ '//textLearn//models//LR//UP//LR_model'
            pickle.dump(lr, open(filename, 'wb'))  
        else:
            logging.info('{time}_UP_UP-模型沒超過80%，所以沒更新'.format(time=now_str_datetime))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])#main(ip, user, passw)














