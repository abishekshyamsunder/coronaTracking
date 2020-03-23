import os
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from twisted.internet import task, reactor
import matplotlib.pyplot as plt
tval=0
driver = webdriver.Chrome()

counter1=[]
time=[]
timeout = 60.0

def doWork():
	global tval
	tmp = tval
	tval = tmp + 1
	driver = webdriver.Chrome()
	link1='https://www.worldometers.info/coronavirus/#countries'
	link2='https://www.worldometers.info/coronavirus'
	link=link2
	check=True
	nol=0
	while(check):
		driver.get(link)
		content = driver.page_source
		f=open('temp.temp','w')
		f.write(content)
		f.close()
		f=open('temp.temp','r')
		while(True):
			line=f.readline()
			if not line:
				break
			nol=nol+1
		if nol>3000:
			check=False
		else:
			if link==link1:
				link=link2
			else:
				link=link1
	f=open('temp.temp','r')
	next = False
	while(True):
		line=f.readline()
		if not line:
			break
		x = re.search('India',line)
		if x and next==False:
			next=True
		elif x and next==True:
			break
	line=f.readline()
	temp = re.search(">.*<",line)
	line2=line[temp.start()+1:temp.end()-1]
	line2=int(line2)
	time.append(tval)
	counter1.append(line2)
	f.close()
	os.remove('temp.temp')
	driver.close()
	plt.plot(time, counter1)
	plt.xlabel('Minutes from start')
	plt.ylabel('Cases in India')
	#print(time,counter1)
	plt.show(block=False)
	plt.pause(3)
	plt.close()
	#print(line2)
	pass

l = task.LoopingCall(doWork)
l.start(timeout) # call every sixty seconds
reactor.run()