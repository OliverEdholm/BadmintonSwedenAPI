# imports
from .utils import get_soup

import logging
import configparser

# setup
logger = logging.getLogger('badmintonswedenapi')

config = configparser.ConfigParser()
config.read('config.ini')


# functions
def search_player(query):
    logger.info('getting players that match query: {}'.format(query))

    if len(query) < 2:
        return None

    url = config['urls']['player_search_url'].format(
        query=query
    )

    soup = get_soup(url)

    player_tags = soup.findAll('li', {'class': 'list-ui__item'})

    player_data = []
    for tag in player_tags:
        h4_tag = tag.findAll('h4', {'class': 'media__title'})[0]
        a_tag = h4_tag.a

        name = a_tag['title']
        url = config['urls']['main'] + a_tag['href'][1:-4]
        iid = h4_tag.span.text[2:-1]

        data = {
            'name': name,
            'url': url,
            'iid': iid
        }

        player_data.append(data)

    return player_data
