def write(title,data):
	import os
	out = open(title + '.html','w',encoding='utf-8')
	print (data,file=out)
	out.close
	
def parser(url):
	import urllib.request
	import re
	
	htmlBytes = urllib.request.urlopen(url).read()
	html = htmlBytes.decode('UTF-8')
	
	title = re.compile(r'<h2.+?>\s+(?:<a href=".+?">)?(.+?)(?:</a>)?\s+</h2>.+?<a class="author-link" data-tip=".+?>(.+?)</a>.+?<div class="zm-item-vote-info " data-votecount="(\d+)".+?<div class="zm-editable-content clearfix">\s+(.+?)</div>',re.DOTALL)
	contentArray = title.findall(html)
	
	content = '<h2 align="center">'+contentArray[0][0]+'</h2><br><span style="float:right;">赞数：'+contentArray[0][1]+'</span><br><span style="float:right;">作者：'+contentArray[0][2]+'</span><br><br>'+contentArray[0][3]
	
	write(contentArray[0][0],content)
	

def com():
	import sys
	print("请输入知乎问题页面的URL")
	print("例如：http://www.zhihu.com/question/26125708")
	line = sys.stdin.readline()
	parser(line)
	
com()