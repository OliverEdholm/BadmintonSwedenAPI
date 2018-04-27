# imports
import requests
from bs4 import BeautifulSoup


# functions
def get_soup(url):
    html = requests.get(url).text

    return BeautifulSoup(html, 'html.parser')
