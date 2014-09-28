from multiprocessing import Process, Queue, Pool
from subprocess import call
import sys
import re, codecs, Queue, os
import time

ScrapeQueue = Queue.Queue()

def fork(toDo):
	name = "%s"%(toDo).replace(".py","")
	dir = os.getcwd()
	os.chdir(dir)
	sys.stdout = open('log-timestamp.csv','a')
	start = time.time()
	print "Acquired: %s"%(toDo), start
	print call(["python", name + ".py"])
	print "Completed %s"%(toDo)
	print "Number of rows:", open('%s_20140928_000.csv'%(name), 'r').read().count("\n")
	print "Completed in:", str(time.time() - start)

if __name__ == '__main__':
	p = Pool(1)
	ScrapeQueue = []
	i=1
	for line in codecs.open("SD.SFcsf.txt","r","utf-8"):
		ScrapeQueue.append(line.strip())
	print ScrapeQueue
	p.map(fork, ScrapeQueue)
