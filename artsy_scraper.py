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
                s=requests.session()
                s.headers['X-XAPP-TOKEN'] = self.token
                res = s.get(CATEGORY_API_URL.format(page=str(page), category=category))

                if not res.ok:
                    break
                records.append(res.json())
        return pd.concat([pd.DataFrame(rec) for rec in records])


new_token = 'JvTPWe4WsQO-xqX6Bts49j4qtAO9fjV00DNgW56CqJEuwKHVWR1Zlytn5uxbK-znaA5-RyqbQLwZb_aR-P4tMkl1nzNUBWKxRCxAR57AQyejbfDdrhGLa5_ZdEP-TY1fzYgBZkC_ZaWY15GDXrN5eC3rU7AqSsAetQ53ioH5FrkZmgC7qo4UPkuXRio1NuOio6GegvGO5U1jz38qRkL60CDPR5FiV661XdYnLGOn2BQ='
test = ArtsyScraper(new_token)

test.get_artworks_by_categories(categories = DEFAULT_CATEGORIES, max_results_per_category = 200)