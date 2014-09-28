from multiprocessing import Process, Queue, Pool
from subprocess import call
import sys
import re, codecs, Queue, os
import time
stamp = time.strftime("%Y%m%d")

ScrapeQueue = Queue.Queue()

def fork(toDo):
	name = "%s"%(toDo).replace(".py","")
	dir = os.getcwd()
	os.chdir(dir)
	sys.stdout = open('log_%s.txt'%(stamp),'a')
	print dir
	print "Feed to aggregate: %s"%(toDo)
	start = time.time()
	print call(["python", name + ".py"])
	print "Completed %s"%(toDo)
	print "Number of records:"
	print open('%s_%s_000.csv'%(name,stamp), 'r').read().count("\n")
	print "Completed in:"
	print str(time.time() - start)

if __name__ == '__main__':
	p = Pool(1)
	ScrapeQueue = []
	i=1
	for line in codecs.open("sourcelist.txt","r","utf-8"):
		ScrapeQueue.append(line.strip())
	print ScrapeQueue
	p.map(fork, ScrapeQueue)
