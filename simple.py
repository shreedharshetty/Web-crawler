import re
from urllib2 import urlopen
import sqlite3
db = sqlite3.connect('test2.db')
db.row_factory = sqlite3.Row
db.execute('drop table if exists test')
db.execute('create table test(id INTEGER PRIMARY KEY,url text)')
# Since few href may return only /contact or /about, concatenate to baseurl.
def concat(url, baseurl): 
    if url.find('http://'):
        url = baseurl + url
        return url
    else:
        return url

def get_links(baseurl):
    resulting_urls = set()
    try:
        # Check whether the url contains .msi extensions.
        if baseurl.find('.msi') == -1:
            # Parse htmlSource and find all anchor tags.
            htmlSource = urlopen(baseurl).read()
            htmlSource = htmlSource.decode("iso-8859-1")

            # Returns href and other attributes of a tag.
            linksList = re.findall('<a href=(.*?)>.*?</a>',htmlSource)

            for link in linksList:
                # Setting start and end points in the link.
                start_quote = link.find('"')
                end_quote = link.find('"', start_quote + 1)

                # Get the string between start_quote and end_quote.
                url = link[start_quote + 1:end_quote]

                url_after_concat = concat(url, baseurl)
                resulting_urls.add(url_after_concat)

        else:
            return True

    except:
        print("failed")

    return resulting_urls
urls =  get_links('http://www.python.org')
for url in urls:
    db.execute('insert or ignore into test(url) values (?)', [url])
    db.commit()
cursor = db.execute('select * from test')
for row in cursor:
        print (row['id'],row['url'])