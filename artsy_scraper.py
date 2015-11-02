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
import math

# maximun number of records per page

RECORDS_PER_PAGE = 100

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
    """
    This exception is raised when there is a bad unauthorized response.
    """
    pass

class HTTPException(Exception):
    """
    This exception is raised when there is a bad response that's other than unauthorized.
    """
    pass

class ArtsyScraper(object):
    """
    This class requests data from the non-publicized artsy API.
    """
    def __init__(self, token):
        self.token = token

    def check_response(self, response):
        """
        This method checks to see whether the response is okay. 
        """
        if response.status_code == requests.codes.unauthorized: 
            raise UnauthorizedException(response.json()['text'])
        elif not response.ok and response.status_code != requests.codes.not_found:
            raise HTTPException(response.json())

    def calculate_pages(self, num_results):
        """
        Calculates the number of pages need to retrieve the of number results needed. 
        """
        pages = num_results / RECORDS_PER_PAGE
        if num_results % RECORDS_PER_PAGE > 0:
            pages = pages + 1 
            
        return pages

    def get_artworks_by_categories(self, categories = DEFAULT_CATEGORIES, max_results_per_category = 10000):
        """
        This method sends a request to the artsy.net API and scrapes data based on the desired categories and number of results.
        """
        records = [] 

        pages = self.calculate_pages(max_results_per_category)
        
        for category in categories:
            for page in xrange(1, pages + 1):
                session = requests.session()
                session.headers['X-XAPP-TOKEN'] = self.token
                response = session.get(CATEGORY_API_URL.format(page = page, category = category))

                self.check_response(response)

                if response.status_code == requests.codes.not_found:
                    break

                records.extend(response.json()[0:(max_results_per_category - len(records))])

        return records
        # int(math.ceil(1.0 * max_results_per_category / 100))
        #+ ((max_results_per_category % 100) ? 1 : 0)


new_token = 'JvTPWe4WsQO-xqX6Bts49r4tDJjzicy22lNK9c5bmBQPI_yNHMdjMnqszvPZF7d404olH4KJB1bznv0nIfKjHmCqCKTyjqs0a9OPasF3xyMAv1X0VuPULZNcPmV5HnZPZjaeTqfThBqy2CrUUqHzaIQzI7W7EmiHSuyyKD9MXvxOfJDYPc4aNBzt2pWjt3rJ_K6Te5rOjn2fp-1iEgh368c2q7sjVsgBm4I32rLYe5A='
test = ArtsyScraper(new_token)

art = test.get_artworks_by_categories(categories = DEFAULT_CATEGORIES, max_results_per_category = 200)
print art