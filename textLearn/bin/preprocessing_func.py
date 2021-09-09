from jieba import lcut
import pandas as pd
import numpy as np
import string
from scipy.sparse import csr_matrix
from textLearn.bin.patch import ComplainConditionAdjust
#preprocessing for up
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
    ls_of_wid = np.array(ls_of_wid)
    return ls_of_wid

def add_feature(sr):
    num_only = int(sr.isdigit())
    abc_only = int(sr.encode( 'UTF-8').isalpha())
    return [num_only, abc_only]

def change_the_type_fitmodel(text, dict_key):
    result = [lcut(text)]
    tmp = []
    for i in result[0]:
        if i in dict_key:
            tmp.append(i)
    result = [tmp]       
    return result  

def add_feature2(text):
    strs_df = pd.DataFrame({'message':[text]})
    strs_df['char_count'] = strs_df['message'].apply(len)
    strs_df['word_count'] = strs_df['message'].apply(lambda x: len(x.split()))
    strs_df['word_density'] = strs_df['char_count'] / (strs_df['word_count']+1)
    strs_df['punctuation_count'] = strs_df['message'].apply(lambda x: len("".join(_ for _ in x if _ in string.punctuation)))                 
    return strs_df[['word_count', 'word_density', 'punctuation_count']].values      

def remove_punctuation(s): 
    punctuation = '''''表情\n!！()-[]{};:'"\,<>./[email protected]#$%^&*_~'''+ string.whitespace+ string.punctuation
    my_str = s 
    no_punct = "" 
    for char in my_str: 
        if char not in punctuation: 
            no_punct += char 
    return(no_punct) 

def get_train(text, dictionary, tv, maxminscaler):
    dict_key = list(dictionary.keys())
    text_1 = change_the_type_fitmodel(text, dict_key)          
    text_1 = vectorize(text_1, dictionary)
    text_1 = np.c_[text_1, 
                   np.array(add_feature(text)).reshape((1, 2)), 
                   tv.transform(pd.Series(text)).toarray(),
                   add_feature2(text)]
    result = maxminscaler.transform(text_1)
    return result

def Get_Json_result(model, labeldict, df, keyWords, feature, complain_sentiment, control, br_rate=1, cf_rate=1):
    classPossibility = model.predict_proba(df)
    probsarg = [str(x) for x in classPossibility.argsort()[0][-3:][::-1] + 1]
    label = int(probsarg[0])
    if control == 'BC':
        probs = [classPossibility[0][int(x) - 1] for x in probsarg]        
        labelMeaning = labeldict[label]
        top3ClassPossibility = {int(a): b for a, b in zip(probsarg, probs)}
        result = {
            'businessRelated': int(probs[0] > 0.25*br_rate),
            'classConfident': int(probs[0] > 0.5*cf_rate),
            'keyWords': keyWords,
            'feature': feature,
            'label': int(label),
            'labelMeaning': labelMeaning,
            'classPossibility': classPossibility[0].tolist(),
            'top3ClassPossibility': top3ClassPossibility,
            'sentiment': {
                'compalin_detail': complain_sentiment
            },
        }
        result = ComplainConditionAdjust(result)
    elif control == 'UP':
        probsarg_notincludingNoMEANING = [str(x) for x in classPossibility[0][0:-1].argsort()[-3:][::-1] + 1]           
        probs = [classPossibility[0][int(x) - 1] for x in probsarg_notincludingNoMEANING]  
        if label == 7:
            labelMeaning = None
        else:
            labelMeaning = labeldict[label]     
        top3ClassPossibility = {int(a): b for a, b in zip(probsarg_notincludingNoMEANING, probs)}          
        result = {
            #'businessRelated': int(np.max(classPossibility[0][0:-1]) > 0.25),#int(label != 7),
            'businessRelated': int(np.max(classPossibility[0]) > 0.25),#int(label != 7),            
            'classConfident': int(max(probs) > 0.5),
            'keyWords': keyWords,
            'feature': [3],
            'label': label,
            'labelMeaning': labelMeaning,
            'classPossibility': classPossibility[0].tolist(),
            'top3ClassPossibility': top3ClassPossibility,
            'sentiment': {
                'compalin_detail': complain_sentiment
            },
        }
    return result

def Return_none(complain_sentiment):
    ret = {'businessRelated': 0,
           'classConfident': None,
           'keyWords': None,
           'feature': None,
           'label': None,
           'labelMeaning': None,
           'classPossibility': None,
           'top3ClassPossibility': None,
           'sentiment': {
           'compalin_detail': complain_sentiment},}
    return ret