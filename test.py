#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Ziqi on 18-3-12
# This is the test script in the textLearn project.

import textLearn
from textLearn import tc

if __name__ == '__main__':

    ret = tc.predict("我要存款", textLearn.LRModel)
    
    for k, v in ret.items():
    	print (k, ': \n', v, '\n')

    import json
    a = json.dumps(ret)
    print(a)
    print(json.loads(a))
