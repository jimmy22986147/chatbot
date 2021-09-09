#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-5
# This is the basic script in the textLearn project.

import re
import math
from scipy.sparse import coo_matrix, vstack, hstack

table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０',
     u',.!?[]()%#@&1234567890')}

def Flatten(a):
    '''

    :param a: a list with a complex structure
    :return: a flatten list that all objects lying in the lowest level.
    '''
    for each in a:
        if not isinstance(each, list):
            yield each
        else:
            yield from Flatten(each)

def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]

def OnlyChinese(s):
    '''

    :param s: a str object
    :return: only Chinese characters in s
    '''
    s = s.translate(table)
    return re.sub(u"[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\ ,\。\、\？\“\”\：\；\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", s)


def OnlyGoodString(s):
    '''

    :param s: a str object
    :return: only Chinese characters in s
    '''
    return re.sub(u"(amp)|(nbsp)|[\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", s)


def Sparsely(feature, nKeyWords):
    tempData = [1] * len(feature)
    row = [0] * len(feature)
    col = feature

    feature = coo_matrix(
        (tempData, (row, col)), shape=(1, nKeyWords)
    ).tocsr()
    return feature
