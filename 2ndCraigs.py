import urllib2, feedparser, sys
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin


pwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
pwdmgr.add_password("New mail feed", 'http://mail.google.com/', "insurgasaurus", "****")
auth = urllib2.HTTPBasicAuthHandler(pwdmgr)
opener = urllib2.build_opener(auth)

BASE_URL = 'https://sfbay.craigslist.org/scz/'

def scrape_missed_connections():
    response = requests.get(BASE_URL + "sss/")
    soup = BeautifulSoup(response.content)
    missed_connections = soup.find_all('span', {'class':'pl'})

    count = 0
    w = open('newblacklist', 'w')
    f = open('blacklist', 'r')
    blacklist = f.readlines()
    print('just about to ')
    #this for loop is only giving me the last thing in the file, not a list of everything
    for i in blacklist:
	blacklist = i.strip('\n')
	#print('right here son')
	#print('current blacklisted url: ' + i)
    print(blacklist)
    f.close()
    
    w = open('blacklist', 'w')

    for missed_connection in missed_connections:
        link = missed_connection.find('a').attrs['href']
        url = urljoin(BASE_URL, link)
        temp_url_toblack = scrape_missed_connection(url, blacklist)
	temp_url_toblack = str(temp_url_toblack)
	temp_url_toblack = temp_url_toblack.strip('None')
	#print(newblacklist)
	if(temp_url_toblack):
	   w.write(temp_url_toblack + '\n')
	count += 1
    print(count)
    w.close()

def scrape_missed_connection(url, blacklist):
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    data = {
        'source_url': url,
        'subject': soup.find('h2', {'class':'postingtitle'}).text.strip(),
        'body': soup.find('section', {'id':'postingbody'}).text.strip(),
        'datetime': soup.find('time').attrs['datetime']
    }
    temp = str(data['subject'])
    if 'BOOK' in temp:	
	print("found")
	if data['source_url'] not in blacklist:
		print("valid")
		return(data['source_url'])
		
	else:
	    print("not valid")
	print(data['source_url'])
    #print(data['source_url'])
    #print(type(data['subject']))
    #print(type(str(data['subject'])))
    #print(data['subject'])  
    #pprint(data)



#blacklist=[]
#blacklist.append('url')
#print(blacklist[0])

if __name__ == '__main__':
    scrape_missed_connections()
    #scrape_missed_connections()











