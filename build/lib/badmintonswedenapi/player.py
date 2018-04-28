# imports
from .utils import get_soup

import os
import configparser

import maya

# setup
config = configparser.ConfigParser()
config.read('config.ini')


# functions
def get_non_played_tournaments(player_url):
    def get_relevant_soups(current_year):
        def get_tournaments_soup(year):
            year_query = '?{tournament_year_query}={year}'.format(
                tournament_year_query=config['url_querys']['tournament_year'],
                year=year
            )

            tournaments_url = os.path.join(
                player_url,
                config['url_extensions']['player_tournaments'],
                year_query
            )

            return get_soup(tournaments_url)

        def get_tournament_years(soup):
            tournament_tabs = soup.findAll('ul', {'id': 'tabs_tournaments'})[0]
            tabs = tournament_tabs.findAll(
                'li', {'class': 'page-nav__item js-page-nav__item'})

            years = []
            for tab in tabs:
                year_text = tab.a.text
                if year_text != 'Äldre':
                    year = int(year_text)
                    years.append(year)

            return years

        soups = {
            current_year: get_tournaments_soup(current_year)
        }

        tournament_years = get_tournament_years(soups[current_year])
        for year in tournament_years:
            if year > current_year:
                soup = get_tournaments_soup(year)
                soups[year] = soup

        return soups.values()

    def get_tournaments(soup):
        tournament_divs = soup.findAll(
            'div', {'class': 'media media--padded has-icons-on-hover'})

        tournaments = []
        for div in tournament_divs:
            name = div.h4.a.text

            extension = div.a['href']
            url = config['urls']['main'] + extension[1:]

            time_tags = div.findAll('time')
            start_date = maya.parse(time_tags[0].text)
            if len(time_tags) == 1:
                end_date = start_date
            else:
                end_date = maya.parse(time_tags[1].text)

            tournament = {
                'name': name,
                'url': url,
                'start_date': start_date,
                'end_date': end_date
            }
            tournaments.append(tournament)

        return tournaments

    def extract_non_played_tournaments(tournaments):
        def is_non_played(tournament):
            return tournament['start_date'] >= current_date

        non_played_tournaments = []
        for tournament in tournaments:
            if is_non_played(tournament):
                non_played_tournaments.append(tournament)

        return non_played_tournaments

    current_date = maya.now()
    current_year = current_date.year

    relevant_soups = get_relevant_soups(current_year)

    all_non_played_tournaments = []
    for soup in relevant_soups:
        tournaments = get_tournaments(soup)
        non_played_tournaments = extract_non_played_tournaments(tournaments)

        all_non_played_tournaments.extend(non_played_tournaments)

    all_non_played_tournaments = sorted(all_non_played_tournaments,
                                        key=lambda x: x['start_date'],
                                        reverse=True)

    return all_non_played_tournaments
