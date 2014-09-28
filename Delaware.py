from bs4 import BeautifulSoup
from pymongo import Connection
import requests
from selenium import webdriver
from thready import threaded

browser = webdriver.Chrome() 
browser.get('https://dpronline.delaware.gov/mylicense%20weblookup/Search.aspx?facility=Y')

host = 'localhost'
database = 'lotto'
collection = 'Delaware'


def mongo_connection():
	con = Connection(host)
	col = con[database][collection]
	return col

print browser.current_url
col = mongo_connection()


def george_washington(url):
	browser.get(url)
	dict = {}
	source = browser.page_source 
	soup = BeautifulSoup(source)
	dict['url'] = browser.current_url 
	dict['name'] = soup.findAll("span", {"id" : "_ctl16__ctl1_full_name"})[0].text
	dict['licno'] = soup.findAll("span", {"id" : "_ctl21__ctl1_license_no"})[0].text
	dict['prof'] = soup.findAll("span", {"id" : "_ctl21__ctl1_profession_id"})[0].next
	dict['lic_status'] = soup.findAll("span", {"id" : "_ctl21__ctl1_sec_lic_status"})[0].next
	dict['issue_date'] = soup.findAll("span", {"id" : "_ctl21__ctl1_issue_date"})[0].next
	dict['expiration_date'] = soup.findAll("span", {"id" : "_ctl21__ctl1_expiration_date"})[0].next
	dict['city'] = soup.findAll("span", {"id" : "_ctl26__ctl1_addr_city"})[0].next
	dict['state'] = soup.findAll("span", {"id" : "_ctl26__ctl1_addr_state"})[0].next
	dict['zipcode'] = soup.findAll("span", {"id" : "_ctl26__ctl1_addr_zipcode"})[0].next
	dict['country'] = soup.findAll("span", {"id" : "_ctl26__ctl1_addr_country"})[0].next
	col.insert(dict)
	print dict

	
def delaware_river():
	links = []
	for i in range(1000,100000):
		url = "https://dpronline.delaware.gov/mylicense weblookup/Details.aspx?agency_id=1&license_id=%d&"%i
		links.append(url)
	threaded(links, george_washington, num_threads=20)

if __name__ == '__main__':
    delaware_river()