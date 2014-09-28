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
	sys.stdout = open('%s.txt'%(name),'w')
	print dir
	print "Acquired scrape: %s"%(toDo)
	start = time.time()
	print call(["python", name + ".py"])
	"""cfile = re.compile("^.*csv$")
	for fname in os.listdir(dir + "/"):
		if cfile.match(name):
			csvfile = fname
			print csvfile"""
	print "Completed %s"%(toDo)
	#print "Filename written:"
	#print csvfile
	print "Number of rows:"
	print open('%s_20140928_000.csv'%(name), 'r').read().count("\n")
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
