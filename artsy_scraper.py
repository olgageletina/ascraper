"""
.. module:: artsy_scraper.py
   :synopsis: This scraper is designed to scrape the information on artworks available on artsy.net. This script returns JSON records.

.. moduleauthor:: Olga Geletina (under tutelage of Jon Kaczynski)

Docstring for my module

.. data:: RECORDS_PER_PAGE
    
    Maximum number of records per page

.. data:: CATEGORY_API_URL

    The API URL used as input for get_artworks_by_categories to scrape artworks
    
.. data:: DEFAULT_CATEGORIES
    
    Enumerates various artwork categories, used as input for get_artworks_by_categories to scrape artworks 

more specifically, the browse home page: 'https://www.artsy.net/browse'. 
compared to the information attained using the artsy API, the scraper results are more numerous -- the resulting dataset ranges between 60,000 - 70,000 records.
"""

import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import StringIO
import html5lib
import getpass
import math

RECORDS_PER_PAGE = 100

CATEGORY_API_URL = 'https://api.artsy.net/api/v1/search/filtered/gene/{category}?size=100&page={page}'

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

class UnauthorizedException(Exception):
    """
    .. class:: UnauthorizedException
        This exception is raised when there is a bad unauthorized response.

    """
    pass

class HTTPException(Exception):
    """
    .. class:: HTTPException
        This exception is raised when there is a bad response that's other than unauthorized.

    """
    pass

class ArtsyScraper(object):
    """
    .. class:: ArtsyScraper
        This class requests data from the non-publicized artsy API.

    """
    def __init__(self, token):
        self.token = token

    def check_response(self, response):
        """
        This method checks to see whether the response is okay.
        
        :param response: HTTP response from the server.
        :returns: Response object.
        :raises: UnauthorizedException, HTTPException

        """
        if not response.ok:
            if response.status_code == requests.codes.unauthorized: 
                raise UnauthorizedException(response.json()['text'])
            elif response.status_code != requests.codes.not_found:
                raise HTTPException(response.json())
        else:
            return response

    def calculate_pages(self, num_results):
        """
        This method calculates the number of pages need to retrieve the of number results needed.
        
        :param num_results: total number of results to be returned.
        :type num_results: int.
        :returns: int

        """
        pages = num_results / RECORDS_PER_PAGE
        if num_results % RECORDS_PER_PAGE > 0:
            pages = pages + 1 
            
        return pages

    def get_artworks_by_categories(self, categories = DEFAULT_CATEGORIES, max_results_per_category = 10000):
        """
        This method sends a request to the artsy.net API and scrapes data based on the desired categories and number of results.
        
        :param categories: categories of artworks on artsy.net, by default the :const DEFAULT_CATEGORIES: is used.
        :type categories: list.
        :param max_results_per_category: the maximum number of results wanted.
        :type max_results_per_category: int.
        :returns: JSON records

        """
        records = [] 

        pages = self.calculate_pages(max_results_per_category)
        
        for category in categories:
            for page in xrange(1, pages + 1):
                session = requests.session()
                session.headers['X-XAPP-TOKEN'] = self.token
                response = session.get(CATEGORY_API_URL.format(page = page, category = category))

                self.check_response(response)

                #: if after attaining results we get a 404 NOT_FOUND response then there aren't anymore artworks for that category
                if response.status_code == requests.codes.not_found:
                    break

                records.extend(response.json()[0:(max_results_per_category - len(records))])

        return records
        # int(math.ceil(1.0 * max_results_per_category / 100))
        #+ ((max_results_per_category % 100) ? 1 : 0)


#TODO: if __name__ == '__main__':
new_token = 'JvTPWe4WsQO-xqX6Bts49n14lPUtpcfyx0tYwY0RmR_WHGS9UXT9ioTrGP348dTkHkvzkKYYMFIGvaC5my04IcIxUPz0x729rnT7LcQfjF_up7IIQPhTt_4zI0gVerPf3LXVtRrh3l12Ob8EqJ6HQ2MJIUe9SMqqqgK4Mg40NCk9lC82BHrqtOfiZvyEw6XAFZ-x2F7nuJmS07ErJRNwb9IeV7vtPJSLe5kPWOtcVmM='
test = ArtsyScraper(new_token)
art =  test.get_artworks_by_categories(categories = DEFAULT_CATEGORIES, max_results_per_category = 200)
print art
#
