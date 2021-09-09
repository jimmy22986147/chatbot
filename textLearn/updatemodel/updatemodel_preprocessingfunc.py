#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jieba import lcut
import sys
import numpy as np
import pandas as pd
'''Function zone'''  
def Getwrongdata(sqlconnect, now_str, now_str_datetime, user, control='test'):    
    if user == 'UP':
        to_db='storeforupdatemodel.PastMessageRecordUP'
        equalornot = '='
    elif user == 'BC':
        to_db='storeforupdatemodel.PastMessageRecordBC'
        equalornot = '!='
    table = "tenant_0001.t_dialogue_record_{now_str}".format(now_str=now_str)
    sqlquery_for_wrong = "SELECT dr.ID,\
                                 dr.DIALOGUE_CONTENT,\
                                 qt2.QUESTION_TYPE_NAME QUESTION_TYPE,\
                                mm.AI_USER USER,\
                                 mm.AI_PRODUCT PRODUCT\
                          FROM  {table} AS dr\
                          LEFT JOIN tenant_0001.t_question_type AS qt \
                          ON dr.QUESTION_TYPE = qt.QUESTION_TYPE_ID\
                          LEFT JOIN tenant_0001.t_question_type AS qt2 \
                          ON dr.MARK_INTENT = qt2.QUESTION_TYPE_ID\
                          LEFT JOIN (SELECT a.PRODUCT_ID,\
                                              a.MODEL_NAME,\
                                              b.AI_USER, \
                                              b.AI_PRODUCT\
                                       from tenant_0001.t_product AS a\
                                       LEFT JOIN tenant_0001.t_model_config AS b\
                                       ON a.MODEL_NAME = b.MODEL_NAME )mm\
                          ON dr.PRODUCT_ID = mm.PRODUCT_ID\
                          WHERE qt2.QUESTION_TYPE_NAME IS NOT NULL  \
                          AND qt.QUESTION_TYPE_NAME != qt2.QUESTION_TYPE_NAME\
                          AND dr.UPDATE_TIME IS NOT NULL\
                          AND dr.AI_STATUS IS NULL\
                          AND mm.AI_USER {equalornot} 'UP'\
                          AND dr.UPDATE_TIME >= (SELECT MAX(updateDAY) FROM storeforupdatemodel.PastMessageRecordBC)".format(table=table,
                                                                                                                             equalornot=equalornot)
    
    data_for_wrong = sqlconnect.MySQLQuery(sqlquery_for_wrong)
    if data_for_wrong.empty:
        print('無資料新增')
        #sys.exit()
        before_data, recent_data = pd.DataFrame(), pd.DataFrame()
    else:
        
        if control == 'prod':  
            data_for_wrong_insert = data_for_wrong.copy()
            data_for_wrong_insert.loc[:, 'Complain'] = 0
            data_for_wrong_insert.loc[:, 'weight'] = 1
            data_for_wrong_insert.loc[:, 'updateDAY'] = now_str_datetime
            
            data_for_wrong_insert = data_for_wrong_insert[['DIALOGUE_CONTENT', 'QUESTION_TYPE', 'Complain', 'weight', 'updateDAY',\
                                                           'USER', 'PRODUCT']]
            sqlconnect.MySQLExemany(data_for_wrong_insert, 
                                    to_db,
                                    data_for_wrong_insert.columns)        
            if data_for_wrong.shape[0] == 1:
                condition_string = '= {}'.format(data_for_wrong['ID'][0])
            elif data_for_wrong.shape[0] >= 1:
                condition_string = 'in {}'.format(tuple(data_for_wrong['ID']))
            Update_string = "Update {table} set AI_STATUS=1, AI_TIME='{time}' WHERE ID {condition}".format(table=table,
                                                                                                           time= now_str_datetime,
                                                                                                           condition=condition_string)
            sqlconnect.MySQLUpdate(Update_string)        
            
            sqlquery_for_old = "select DIALOGUE_CONTENT,\
                                       QUESTION_TYPE \
                                FROM {db}\
                                WHERE QUESTION_TYPE IS NOT NULL\
                                      AND QUESTION_TYPE != '抱怨'\
                                      AND updateDAY = '2021/3/25'\
                                GROUP BY DIALOGUE_CONTENT,\
                                         QUESTION_TYPE".format(db=to_db)
            before_data = sqlconnect.MySQLQuery(sqlquery_for_old)

            sqlquery_for_recent = "select DIALOGUE_CONTENT,\
                                       QUESTION_TYPE, USER, PRODUCT \
                                FROM {db}\
                                WHERE QUESTION_TYPE IS NOT NULL\
                                      AND QUESTION_TYPE != '抱怨'\
                                      AND updateDAY >= '2021/3/26'\
                                GROUP BY DIALOGUE_CONTENT, QUESTION_TYPE, USER, PRODUCT".format(db=to_db)
            recent_data = sqlconnect.MySQLQuery(sqlquery_for_recent)
    
    return data_for_wrong, before_data, recent_data


def train_12or26(data, labelDict, old2newLabelMap, newLabelDict, form='OldStr_OldEncoding'):
    df = data.copy()
    labelDict_verse = dict(zip(labelDict.values(), labelDict.keys()))
    newLabelDict_verse =  dict(zip(newLabelDict.values(), newLabelDict.keys()))
    if form == 'OldStr_OldEncoding':
        change = []
        for i in range(df.shape[0]):
            temp = labelDict_verse[df.QUESTION_TYPE[i]]
            change.append(temp)
    elif form == 'OldStr_NewEncoding':
        change = []
        for i in range(df.shape[0]):
            temp = labelDict_verse[df.QUESTION_TYPE[i]]
            change.append(old2newLabelMap[temp])
    elif form == 'NewStr_NewEncoding':
        change = []
        for i in range(df.shape[0]):
            temp = newLabelDict_verse[df.QUESTION_TYPE[i]]
            change.append(temp)        
    df.loc[:, 'label'] = change      
    return df



#pre-processing function
def vectorize(ls_of_words, dt):
    length = len(dt)
    # 句向量
    ls_of_wid = []
    for words in ls_of_words:#ls_of_words 
        vector = [0] * length
        for word in words:
            try:
                vector[dt[word]] += 1
            except:
                continue
        ls_of_wid.append(vector) 
    return ls_of_wid

def add_feature(sr):
    num_only = int(sr.isdigit())
    abc_only = int(sr.encode( 'UTF-8').isalpha())
    #numorabc_only = int(sr.isalnum())
    def is_contains_chinese(strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return 1
        return 0
 
    #检验是否全是中文字符
    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return 0
        return 1
    #allchinese = is_all_chinese(sr)
    #containchinese = is_all_chinese(sr)   
    return [num_only, abc_only]


def remove_punctuation(s): 
    punctuation = '''''表情\n!！()-[]{};:'"\,<>./[email protected]#$%^&*_~''' #'''''\n!()-[]{};:'"\,<>./[email protected]#$%^&*_~！（）－［］｛｝；：’＂＼，＜＞．／＃＄％︿＆＊＿～'''
    my_str = s 
    no_punct = "" 
    for char in my_str: 
        if char not in punctuation: 
            no_punct += char 
    return(no_punct) 


def change_the_type_fitmodel(text, dict_key):
    result = [lcut(text)]
    tmp = []
    for i in result[0]:
        if i in dict_key:
            tmp.append(i)
    result = [tmp]       
    return result  


def size_of_data(data, unit='MB'):
    mem = sys.getsizeof(data) 
    if unit == 'GB':
        res = mem/(1024*1024*1024)
    elif unit == 'MB':
        res = mem/(1024*1024)
    print('data memory: {}{}'.format(str(res), unit))


def Random_choice_sample(data, size):
    np.random.seed(1234)
    if data.shape[0] < size:
        replace = True
    else:
        replace = False        
    r0 = list(np.random.choice(data.shape[0], 
                               size=size,
                               replace=replace,
                               p=None))
    result = data.iloc[r0, :].reset_index(drop=True)
    return result


