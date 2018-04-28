# imports
import logging

import requests
from bs4 import BeautifulSoup

# setup
logger = logging.getLogger('badmintonswedenapi')


# functions
def get_soup(url):
    logger.debug('getting soup from url: {}'.format(url))
    html = requests.get(url).text

    return BeautifulSoup(html, 'html.parser')
