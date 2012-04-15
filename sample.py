import re
import urllib.request
import sqlite3
db = sqlite3.connect('test1.db')
db.row_factory = sqlite3.Row
db.execute('drop table if exists test')
db.execute('create table test(id INTEGER PRIMARY KEY,url text)')
#module to vsit the given url and get the all links in that page
def get_links(urlparse):
        try:
            if urlparse.find('.msi') ==-1: #check whether the url contains .msi extensions
                htmlSource = urllib.request.urlopen(urlparse).read().decode("iso-8859-1")  
                linksList = re.findall('<a href=(.*?)>.*?</a>',htmlSource)
                for link in linksList:
                    start_quote = link.find('"')
                    end_quote = link.find('"', start_quote + 1)
                    url = link[start_quote + 1:end_quote]
                    def concate(url):
                        if url.find('http://'):
                            url = (urlparse) + url
                            return url
                        else:
                            return url
                    url_after_concate = concate(url)
                    try:
                        if url_after_concate.find('.tar.bz') == -1:
                            db.execute('insert or ignore into test(url) values (?)', [url_after_concate])
                    except:
                        print("insertion failed")
            else:
                return True
        except:
            print("failed")
get_links('http://www.python.org')
    
cursor = db.execute('select * from test')
for row in cursor:
    print (row['id'],row['url'])
    urlparse = row['url']
    try:
        get_links(urlparse)
    except:
        print ("url error")