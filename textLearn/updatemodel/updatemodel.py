import os
import sys
os.chdir('C://Users//user//Desktop//aicode-master')
wd = os.getcwd()
sys.path.append(wd+ '//Unionfunc//ConnectMySQL')
import ConnectMySQL as ConnectMySQL
import pickle
from datetime import datetime
import numpy as np
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
from sklearn.naive_bayes import MultinomialNB

'''Function zone'''
def Random_choice_sample(data, size, replace=False):
    np.random.seed(1234)
    r0 = list(np.random.choice(data.shape[0], 
                               size=size,
                               replace=replace,
                               p=None))
    result = data.iloc[r0, :].reset_index(drop=True)
    return result

def vectorize(ls_of_words, dt):
    length = len(dt)
    ls_of_wid = []
    for words in ls_of_words:
        vector = [0] * length
        for word in words:
            try:
                vector[dt[word]] += 1
            except:
                continue
        ls_of_wid.append(vector) 
    return ls_of_wid

def size_of_data(data, unit='MB'):
    mem = sys.getsizeof(data) 
    if unit == 'GB':
        res = mem/(1024*1024*1024)
    elif unit == 'MB':
        res = mem/(1024*1024)
    print('data memory: {}{}'.format(str(res), unit))
       
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

def Getwrongdata(sqlconnect, now_str, to_db='storeforupdatemodel.PastMessageRecordBC', control='test'):    
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
                          AND dr.UPDATE_TIME >= (SELECT MAX(updateDAY) FROM storeforupdatemodel.PastMessageRecordBC)".format(table=table)
    data_for_wrong = sqlconnect.MySQLQuery(sqlquery_for_wrong)
    if data_for_wrong.empty:
        print('無資料新增')
        sys.exit()
    else:
        if control == 'prod':  
            data_for_wrong_insert = data_for_wrong.copy()
            data_for_wrong_insert.loc[:, 'Complain'] = 0
            data_for_wrong_insert.loc[:, 'weight'] = 1
            data_for_wrong_insert.loc[:, 'updateDAY'] = datetime.now().strftime('%Y/%m/%d')
            
            
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
                                                                                                           time= datetime.now().strftime('%Y/%m/%d'),
                                                                                                           condition=condition_string)
            sqlconnect.MySQLUpdate(Update_string)        
    print('done')



'''variable zone'''
#sql connect
sqlconnect = ConnectMySQL.MySqlConnect('203.86.236.69', 'jimmyai')
#time
now = datetime.now()
now_str = now.strftime('%Y%m')
#now_str = '202103'


'''train the model'''
#Read wrong info and insert the data to db and update status
Getwrongdata(sqlconnect, 
             now_str, 
             to_db='storeforupdatemodel.PastMessageRecordBC', 
             control='prod')


#Read before data
sqlquery_for_old = "select DIALOGUE_CONTENT,\
                           QUESTION_TYPE \
                    FROM storeforupdatemodel.PastMessageRecordBC\
                    WHERE QUESTION_TYPE IS NOT NULL\
                          AND QUESTION_TYPE != '抱怨'\
                          AND updateDAY = '2021/3/25'\
                    GROUP BY DIALOGUE_CONTENT,\
                             QUESTION_TYPE"
before_data = sqlconnect.MySQLQuery(sqlquery_for_old)
before_data = Random_choice_sample(before_data, 40000, False)



sqlquery_for_recent = "select DIALOGUE_CONTENT,\
                           QUESTION_TYPE \
                    FROM storeforupdatemodel.PastMessageRecordBC\
                    WHERE QUESTION_TYPE IS NOT NULL\
                          AND QUESTION_TYPE != '抱怨'\
                          AND updateDAY >= '2021/3/26'\
                    GROUP BY DIALOGUE_CONTENT, QUESTION_TYPE"
recent_data = sqlconnect.MySQLQuery(sqlquery_for_recent)
recent_data = Random_choice_sample(recent_data, 10000, True)



before_data = train_12or26(before_data, 
                           tc.labelDict,
                           tc.old2newLabelMap, 
                           tc.newLabelDict, 
                           form='OldStr_NewEncoding')
recent_data = train_12or26(recent_data, 
                           tc.labelDict, 
                           tc.old2newLabelMap, 
                           tc.newLabelDict, 
                           form='NewStr_NewEncoding')

data = pd.concat([before_data, recent_data], axis=0)
#data.loc[:, 'DIALOGUE_CONTENT'] = data.loc[:, 'DIALOGUE_CONTENT'].apply(remove_punctuation)
del(before_data, recent_data)



train_list_vec = [lcut(text) for text in data.DIALOGUE_CONTENT]
t_iter = 0
nKeyWords = 8000
dt = dict()
for u, v in enumerate(textLearn.init.Word2Id):
    dt[v] = u
    t_iter += 1
    if t_iter >= nKeyWords:
        break
    
train_list_vec = vectorize(train_list_vec, dt)
train_x, test_x ,train_y, test_y= train_test_split(csr_matrix((train_list_vec), dtype=float),
                                                   data.label,
                                                   test_size=0.2, 
                                                   random_state=1234)


s = time.time()
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
print(time.time()-s)


filename = 'C://Users//user//Desktop//LR_model'
pickle.dump(lr, open(filename, 'wb'))


'''validate the accuracy'''



'''
# 貝葉斯模型訓練
classifier = MultinomialNB()  # 樸素貝葉斯分類器
classifier.fit(train_x, train_y)

# 模型測評
score = classifier.score(test_x, test_y)
print('NB - Test set Accuracy：'+str(round(score*100, 2))+'%')
lr_old = pickle.load(open('C://Users//user//Desktop//aicode-master//textLearn//models//LR//LR_5712_5', 'rb'))
lr_old.score(test_x, test_y)
#save model when accuracy > 80%
filename = 'C://Users//user//Desktop//lr'
pickle.dump(lr, open(filename, 'wb'))
lr2 = pickle.load(open(filename, 'rb'))
def py_env_version_update(iter_add=0.001):
    with open(wd + "\py_version.txt", 'r', encoding='utf-8') as f:
        for lines in f.readlines():
            version = float(lines)
    version = version+iter_add
    with open(wd + "\py_version.txt","w") as f:
        f.write(str(version)[0:5])   
py_env_version_update()
'''















