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
	
	title = re.compile(r'<h2.+?>\s+(.+?)\s+</h2>',re.DOTALL)
	titleArray = title.findall(html)
	
	voteNum = re.compile(r'<div class="zm-item-vote-info " data-votecount="(\d+)"',re.DOTALL)
	voteArray = voteNum.findall(html)
	
	name = re.compile(r'<a class="author-link" data-tip=".+?>(.+?)</a>',re.DOTALL)
	nameArray = name.findall(html)
	
	answer = re.compile(r'<div class="zm-editable-content clearfix">.+?</div>',re.DOTALL)
	answerArray = answer.findall(html)
	
	content = '<h2 align="center">'+titleArray[0]+'</h2><br><span style="float:right;">赞数：'+voteArray[0]+'</span><br><span style="float:right;">作者：'+nameArray[0]+'</span><br><br>'+answerArray[0]
	
	write(titleArray[0],content)
	

def com():
	import sys
	print("请输入知乎问题页面的URL")
	print("例如：http://www.zhihu.com/question/26125708")
	line = sys.stdin.readline()
	parser(line)
	
com()