
#scraping artsy

import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import StringIO
import html5lib
import getpass


ref_url = 'https://www.artsy.net/browse'
i_url = 'https://api.artsy.net/api/v1/search/filtered/main?size=100&page={0}'

# enumerate categories

cats = ['painting', 'work-on-paper', 'photography'
        , 'sculpture', 'design', 'performance-art'
        , 'drawing', 'film-video', 'installation'
        , 'prints', 'jewelry']


# define url

api_url = 'https://api.artsy.net/api/v1/search/filtered/gene/{cat}?size=100&page={page}'


# scrape!

def artsy_scraper(cats, api_url):
    records = []
    for cat in cats:
        for page in xrange(1,100):
        #for url in [api_url.format(str(i)) for i in xrange(1, 1000)]: # how to add a conditional categories?
            s=requests.session()
            s.headers['X-XAPP-TOKEN'] = 'JvTPWe4WsQO-xqX6Bts49qpFKr1f3TyJ-7Qcen1pvBuQ_-8w6eRqPS9L8T2H1Ae-cdz7MYQGPST4uCgoHQloBlM-xdB3yOZEulFRKyQxgDG5bEh30N2CZSqdajZEZHAfXqHI5HRLiRHYP8CwOzJHJiMgNY4tmcvRiGLPllfSrys4tfYmHACGPeSrKZjgo5KuDQd1sgf6NAL17EuAn3OY2Cp9B09JQFtBml3zfnZNEAQ=' 
            res = s.get(api_url.format(page=str(page), cat=cat))

            if not res.ok:
                break
            records.append(res.json())

    # Concat All json pages into single dataframe
    return pd.concat([pd.DataFrame(rec) for rec in records])
    # to get script to run again need to get the new X-APP token


# run function!

artsy_scraper(cats = cats, api_url = api_url)