## textLearn使用说明文档

#### 文本分类接口使用方法：
	
	
	import textLearn
	
	# textClassifier
	tc = textLearn.tc
	# model
	LRModel = textLearn.LRModel
	
	tc.predict(u"为什么我下载app没有领到红包？", LRModel)
	
