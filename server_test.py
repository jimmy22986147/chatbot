#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import textLearn
from textLearn.bin import mainChatDB
from textLearn import tc
import textLearn.bin.chatbot as chatbot
from user_config import user
from flask import Flask
from flask import request
app = Flask(__name__)
    	
@app.route('/hello/')    	
def show_user_profile():
    error = None
    text1 = request.args.get('text1')
    text2 = request.args.get('text2')
    if text2:
        return text1+text2
    elif text1:
        return text1
    else:
        return 'hello'

@app.route('/chatbot/')    	
def route_chatbot():
    text = request.args.get('text')
    ret = chatbot.Chat_Bot(text)
    ret = json.dumps(ret, indent=4, ensure_ascii=False)
    return ret

	
@app.route('/tc/')
def route_predict():
    # show the post with the given id, the id is an integer
    text = request.args.get('text')
    product = request.args.get('product')
    u = request.args.get('user')
    if u is None:
        u = user[0]
    ret = tc.predict(text, textLearn.LRModel[u], product=product, user=u)
    ret = json.dumps(ret, indent=4, ensure_ascii=False)
    return ret

@app.route('/parameter/')
def route_parameter():
    
    ret = dict()    
    user = request.args.get('user')    
    product = request.args.get('product')
    ret['user'] = user
    ret['product'] = product
    ret = json.dumps(ret, indent=4, ensure_ascii=False)
    
    return ret

@app.route('/version/')
def route_version():
    ret = tc.version
    return ret

@app.route('/labelMeaning/')
def route_labelMeaning():
    # show the post with the given id, the id is an integer
    product = request.args.get('product')
    ## Todo patch
    if product.upper() == "UP":
        ret = tc.labelDict_up
    elif product.upper() in ["AICOOL", "AICOOL3", "AI", "AI3"]:
        ret = None
    elif product.upper() == "OLD26":
        ret = tc.labelDict        
    else:
        ret = tc.newLabelDict        
    ret = json.dumps(ret, indent=4, ensure_ascii=False)
    return ret

@app.route('/getWeights/')
def route_getWeights():
    # show the post with the given id, the id is an integer
    word = request.args.get('word')
    u = request.args.get('user')
    if u is None:
        u = user[0]
    ret = tc.getWeights(word, textLearn.LRModel[u])
    ret = json.dumps(ret, indent=4, ensure_ascii=False)
    return ret
    
@app.route('/setWeight/')    	
def route_setWeight():
    if not ('word' in request.args and 'label' in request.args and 'weight' in request.args):
        ret = "网址错误，需正确指定要更改的关键词（word）、目标类别（label）以及权重（weight）及用户(user)"
    else:
        error = None
        word = request.args.get('word')
        u = request.args.get('user')
        if u is None:
            u = user[0]
        label = int(request.args.get('label'))
        weight = float(request.args.get('weight'))
        ret = tc.setWeight(word, label, textLearn.LRModel[u], weight)
    return ret
    
@app.route('/modelUpdate/')    	
def route_modelUpdate():
    if not ('text' in request.args and 'labels' in request.args):
        ret = "网址错误，需正确指定训练语料（text）和目标类别（labels）及用户(user)"
    else:
        error = None
        text = request.args.get('text')
        u = request.args.get('user')
        if u is None:
            u = user[0]
        labels = json.loads(request.args.get('labels'))
        rate = request.args.get('rate')
        if rate:
            ret = tc.modelUpdate(text, labels, textLearn.LRModel[u], float(rate))
        else:
            ret = tc.modelUpdate(text, labels, textLearn.LRModel[u])
    return ret
    
@app.route('/modelReload/')
def route_modelReload():
    modelFileName = request.args.get('modelFileName')
    u = request.args.get('user')
    if u is None:
        u = user[0]
    this_path = textLearn.wd + "/textLearn/models/LR/" + u + "/" + modelFileName
    if os.path.isfile(this_path):
        textLearn.LRModel[u] = textLearn.modelLoader(this_path)
        return f"成功载入模型文件 {modelFileName}" 
    else:
        return f"不存在模型文件 {modelFileName}"
              
@app.route('/modelSave/')
def route_modelSave():
    modelFileName = request.args.get('modelFileName')
    u = request.args.get('user')
    if u is None:
        u = user[0]
    this_path = textLearn.wd + "/textLearn/models/LR/" + u + "/" + modelFileName
    if os.path.isfile(this_path):
        textLearn.modelSaver(textLearn.LRModel[u], this_path)
        return f"成功保存模型文件 {modelFileName}，源文件已被覆盖" 
    else:
        textLearn.modelSaver(textLearn.LRModel[u], this_path)
        return f"成功保存新的模型文件 {modelFileName}"
        
@app.route('/modelList/')
def route_modelList():
    u = request.args.get('user')
    if u is None:
        u = user[0]
    modelList = os.listdir(textLearn.wd + "/textLearn/models/LR/" + u + "/")
    modelList = [dir for dir in modelList if dir.startswith('LR')]
    ret = json.dumps(modelList, indent=4, ensure_ascii=False)
    return ret
