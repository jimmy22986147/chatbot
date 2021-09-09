#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-5
# This is the loader script in the textLearn project.

import json
import pickle


def dataLoader(dir, encoding = 'utf-8'):
    with open(dir, 'r', encoding = encoding) as fp:
        return(json.load(fp))


def dataSaver(object, dir, encoding = 'utf-8'):
    with open(dir, 'w', encoding = encoding) as fp:
        json.dump(object, fp, ensure_ascii=False, indent=4)
        fp.close()

def modelLoader(dir):
    with open(dir, 'rb') as fp:
        return(pickle.load(fp))


def modelSaver(model, dir):
    with open(dir, 'wb') as fp:
        pickle.dump(model, fp)
        fp.close()

