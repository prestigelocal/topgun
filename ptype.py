import json
import requests
import urllib
from bs4 import BeautifulSoup
import re
import codecs
import time
print "Enter Pro Type to QA:"
searched_protype = raw_input("")
print "Scanning for mismatched %s"%(searched_protype)
stamp = time.strftime("%Y%m%d_%H.%M")
f = codecs.open('%s.top200_%s.csv' %(searched_protype,stamp), "w", "utf-8")
s = requests.session()
regex = codecs.open('%s.csv' %(searched_protype),'r','utf-8')
rules = []
for line in regex:
	rule = line.strip().lower().split("|")
	rules.append(rule)
print "Loading match file for %s"%(searched_protype)
lines = [line.strip() for line in regex]
s.get("http://www.porch.com")
badcount = 0
goodcount = 0	
for lane in open("restelectric.csv","r"):
	lane = lane.replace('"', '').strip()
	for i in range(0,200,10):
		url = "http://www.porch.com/search/results?q=%s&%s&offset=%d&rd=25&pr=true" %(searched_protype,lane,i)
		source = s.get(url)
		time.sleep(1)
		soup = BeautifulSoup(source.content)
		urlstring = source.url
		rank = i + 1
		citystate = lane.split("&loc=",1)[1].split("&")[0].replace("%252C",",").replace("%2520"," ")
		name = soup.findAll("div",{"class":"search-results-pro-info"})
		for text in name:
			rank = rank + 1
			info = []
			links = text.findAll("a")
			company = text.findAll("a",{"class":"search-result-pro-name pro-profile-link"})[0].text.strip()
			company_protype = text.findAll("span",{"class":"company-type"})[0].text.strip().replace("/","|")
			links = text.findAll("a")
			for a in links:
				linkstring = a['href']
				if not linkstring in linkstring:
					linkstring = linkstring
			for line in rules:
				if any(word in company.lower() for word in line):
					print "%s - %s: %s" %(rank,citystate,company)
					pass
				else:
					info.append(linkstring)
					info.append(str(rank))
					info.append(citystate)
					info.append(company)
					info.append(company_protype)
					print "\"" + "\"|\"".join(info) + "\"\n"
					f.write("\"" + "\"|\"".join(info) + "\"\n")
f.close()
