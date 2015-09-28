"""
this scraper is designed to scrape the information on artworks available on artsy.net.
more specifically, the browse home page: 'https://www.artsy.net/browse'. 
compared to the information attained using the artsy API, the scraper results are more numerous -- the resulting dataset ranges between 60,000 - 70,000 records.
JSON records are returned.
"""

import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import StringIO
import html5lib
import getpass

# define API URL

CATEGORY_API_URL = 'https://api.artsy.net/api/v1/search/filtered/gene/{category}?size=100&page={page}'

# enumerate categories

DEFAULT_CATEGORIES = ['painting'
                , 'work-on-paper'
                , 'photography'
                , 'sculpture'
                , 'design'
                , 'performance-art'
                , 'drawing'
                , 'film-video'
                , 'installation'
                , 'prints'
                , 'jewelry']

# scrape!
class UnauthorizedException(Exception):
    pass

class HTTPException(Exception):
    pass

class ArtsyScraper(object):
    """
    This class requests data from the non-publicized artsy API.
    """
    def __init__(self, token):
        self.token = token

    def get_artworks_by_categories(self, categories = DEFAULT_CATEGORIES, max_results_per_category = 10000):
        records = []
        for category in categories:
            for page in xrange(1, max_results_per_category / 100):
                session = requests.session()
                session.headers['X-XAPP-TOKEN'] = self.token
                response = session.get(CATEGORY_API_URL.format(page = page, category = category))

                if response.status_code == requests.codes.unauthorized:
                    raise UnauthorizedException(response.json()['text'])

                if not response.ok:
                    #print records
                    print response.json()
                    break
                    #raise HTTPException(response.json())

                records.append(response.json())
                #break

        return records
        #return pd.concat([pd.DataFrame(rec) for rec in records])


new_token = 'JvTPWe4WsQO-xqX6Bts49jf1k5gBrB8xKt4tShB-pfx4_xIuvOwOVBafP5_PgGZh3qfN8V508TmWgs8XWNevka00wQmdqxfcWqQKcchA6UrdFtWkT1L--u5dV5M2Y5SISuCdZcBIT7qn6by-Rtz2msCm9o7J_z85TaP2m-khd9-CsGBbhQX0pakBKDDGU022gpKD6tHK4YTnKf6LrzzS_xl_mCRp-5vFOPylWdUArGg='
test = ArtsyScraper(new_token)

test.get_artworks_by_categories(categories = DEFAULT_CATEGORIES, max_results_per_category = 200)
