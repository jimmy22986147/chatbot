import re

def ComplainConditionAdjust(ret):

	if (ret['classConfident'] == 1) & (ret['label'] == 23):
		
		ret['classConfident'] = 0
		ret['businessRelated'] = 0
		
	return ret
	

def GrammarAdjust(s):
    
    # Rule1
    s = re.sub(u"玩不了|动不了|不能玩|开不了|进不去|不能动|不能开", "打不开", s)
    s = re.sub(u"动态|发言|朋友圈|好友圈", "app", s)
    s = re.sub(u"总输值|输值|总输赢|输赢", "查询状态", s)
    s = re.sub(u"老虎机", "百家乐", s) 
    s = re.sub(u"转不", "不能转帐", s) 
    s = re.sub(u"秒提|提的钱", "提款", s)    
    s = re.sub(u"提不", "提款不", s)
    s = re.sub(u"取不", "取款不", s)
    s = re.sub(u"存不", "存款不", s)
    s = re.sub(u"不了|一下", "", s)
    s = re.sub(u"体育", "游戏", s)
    s = re.sub(u"久安|云闪付|白条|花呗|点卡", "钱包", s)
    s = re.sub(u"不存在|不能登|登不了", "不能登录", s)
    s = re.sub(u"不开心", "郁闷", s)
    s = re.sub(u"多久", "好久", s)
    s = re.sub(u"热门", "推荐", s)    

    return s
