# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import json
import os



class book(object):
	def __init__(self, title, author, publisher, imgUrl, pages):
		self.title = title
		self.author = author
		self.publisher = publisher
		self.imgUrl = imgUrl
		self.pages = pages
	def __str__(self):
		return "\n Title:\t %s\n Author:\t %s\n Publisher:\t %s\n ImgUrl:\t %s\n Pages:\t %s\n" % (self.title, self.author, self.publisher, self.imgUrl, self.pages)

def jdefault(o):
	return o.__dict__

class BKL:
 

	def __init__(self,url):
		self.url = url
		self.books = []
		self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
        #初始化headers
		self.headers = { 'User-Agent' : self.user_agent }

	def getPage(self,pageNum):
		try:
			url = self.url + pageNum
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			content = response.read().decode('utf-8')
			pattern = re.compile('<div.*?grid_24 main_column">.*?<img.*?src="(.*?)&v=.*?</div>.*?grid_10">.*?<h1.*?name">(.*?)</h1>.*?<li.*?=author">(.*?)</a>.*?brand">(.*?)</span>.*?' + u'規格' + '.*?(\d*)'+ u'頁',re.S)
			items = re.findall(pattern,content)
			for item in items:
				#print item[0],item[1],item[2],item[3],item[4]
				bk = book(item[1].encode('utf8'), item[2].encode('utf8'), item[3].encode('utf8'), item[0].encode('utf8'), item[4].encode('utf8'))	
				self.books.append(bk)
				#print bk
			return response
		except urllib2.URLError, e:
			if hasattr(e,"code"):
				print e.code
			if hasattr(e,"reason"):
				print e.reason
			return None

	def goThroughPage(self, start, end):
		for i in range(start, end, -1):
			page = str(i)
			os.system('cls' if os.name == 'nt' else 'clear')
			print float(start-i)/(start-end) #("%fpercent\n" % (i/(end-start)))
			if i < 10:
				self.getPage('001000000' + page)
			elif i < 100 and i >= 10:
				self.getPage('00100000' + page)
			elif i < 1000 and i >= 100:
				self.getPage('0010000' + page)
			elif i < 10000 and i >= 1000:
				self.getPage('001000' + page)
			elif i < 100000 and i >= 10000:
				self.getPage('00100' + page)
			elif i < 1000000 and i >= 100000:
				self.getPage('0010' + page)
		self.writeJSON()

	def writeJSON(self):
		with open('books.json', 'w') as outfile:
			json.dump(self.books, outfile,default=jdefault)


	def start(self):
		start = int(raw_input("輸入起始值"))
		end = int(raw_input("輸入終止值"))
		self.goThroughPage(start, end)
		



 
url = 'http://www.books.com.tw/products/'
bkl = BKL(url)
#bkl.getPage('0010700111')
bkl.start()

