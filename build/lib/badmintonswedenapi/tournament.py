# imports
from .utils import get_soup
from .match import Score
from .match import Match

import logging
import configparser
from datetime import timedelta

import maya

# setup
logger = logging.getLogger('badmintonswedenapi')

config = configparser.ConfigParser()
config.read('config.ini')


# classes
class Tournament(object):
    def __init__(self, name=None, url=None, start_date=None, end_date=None):
        self.name = name
        self.url = url
        self.start_date = start_date
        self.end_date = end_date

    def get_all_matches(self):
        from .player import Player

        def get_match_page_urls():
            def get_day_dates_between(d1, d2):
                delta = d2 - d1

                dates_between = []
                for i in range(delta.days + 1):
                    dates_between.append(d1 + timedelta(days=i))

                return dates_between

            dates_between = get_day_dates_between(
                self.start_date.date,
                self.end_date.date
            )

            urls = []
            for date in dates_between:
                url = '{url}&{date_url_query}={date_without_hyphen}'.format(
                    url=self.url.replace('tournament.aspx', 'matches.aspx'),
                    date_url_query=config['url_querys']['match_page_date'],
                    date_without_hyphen=str(date).replace('-', '')
                )
                urls.append(url)

            dates_between = [maya.parse(str(d))
                             for d in dates_between]

            return urls, dates_between

        def get_match_tags(soup):
            tr_tags = soup.findAll('tr')

            match_tags = []
            for tag in tr_tags:
                if len(tag.findAll('td', {'align': 'center'})) == 1:
                    match_tags.append(tag)

            return match_tags

        def get_match(match_tag, date):
            def get_scheduled_time():
                time_text = match_tag.findAll(
                    'td', {'class': 'plannedtime'})[0].text

                scheduled_time = maya.parse('{date_str} {time_text}'.format(
                    date_str=str(date),
                    time_text=time_text
                ))

                return scheduled_time

            def get_players():
                team1_players = []
                team2_players = []

                tr_tags = match_tag.findAll('tr')
                for tag in tr_tags:
                    a_tags = tag.findAll('a')

                    for a_tag in a_tags:
                        text = a_tag.text.split(' [')[0]
                        if '[' not in text:
                            name = text
                            break
                    else:
                        continue

                    if '[' not in name:
                        player = Player(name=name)

                        if len(tag.findAll('td', {'align': 'right'})) == 1:
                            team1_players.append(player)
                        else:
                            team2_players.append(player)

                return team1_players, team2_players

            def get_seeds():
                team1_seed = ''
                team2_seed = ''

                tr_tags = match_tag.findAll('tr')
                for tag in tr_tags:
                    name_split = tag.a.text.split(' [')

                    if len(name_split) == 2:
                        seed = name_split[1].replace(']', '')

                        if len(tag.findAll('td', {'align': 'right'})) == 1:
                            team1_seed = seed
                        else:
                            team2_seed = seed

                return team1_seed, team2_seed

            def get_score():
                set_spans = match_tag.findAll(
                    'span', {'class': 'score'})
                if len(set_spans) == 0:
                    return Score(sets=[], is_walkover=False)
                else:
                    set_spans = set_spans[0].findAll('span')

                sets = []
                is_walkover = len(set_spans) == 0
                for span in set_spans:
                    text = span.text

                    if any([c not in '1234567890-'
                            for c in text]):
                        is_walkover = True
                    else:
                        team1_score, team2_score = text.split('-')

                        team1_score = int(team1_score)
                        team2_score = int(team2_score)

                        sets.append((team1_score, team2_score))

                score = Score(
                    sets=sets,
                    is_walkover=is_walkover
                )

                return score

            def get_is_played(score):
                is_not_played = score.sets == [] and not score.is_walkover

                return not is_not_played

            scheduled_time = get_scheduled_time()

            team1_players, team2_players = get_players()

            team1_seed, team2_seed = get_seeds()

            score = get_score()

            is_played = get_is_played(score)

            return Match(
                scheduled_time=scheduled_time,
                team1_players=team1_players,
                team2_players=team2_players,
                team1_seed=team1_seed,
                team2_seed=team2_seed,
                score=score,
                is_played=is_played
            )

        logger.info('getting matches from tournament with name: {}'.format(
            self.name))

        urls, dates = get_match_page_urls()

        matches = []
        for url, date in zip(urls, dates):
            soup = get_soup(url)

            match_tags = get_match_tags(soup)
            for tag in match_tags:
                match = get_match(tag, date)

                matches.append(match)

        return matches

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return self.name
