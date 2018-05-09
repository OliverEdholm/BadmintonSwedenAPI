# imports
from badmintonswedenapi.player import Player
from badmintonswedenapi.match import Score
from badmintonswedenapi.match import Match
from badmintonswedenapi.tournament import Tournament

from mock import MagicMock
from collections import Iterable

import maya


# helpers
def assert_mocks_equals_objects(mocks, reals):
    '''Perceive this as a black box :P'''
    def elongate(inp):
        def flatten(items):
            for x in items:
                if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                    yield from flatten(x)
                else:
                    yield x

        if type(inp) is list:
            inp = list(flatten(inp))
        else:
            inp = [inp]

        return inp

    if mocks is None and reals is None:
        return True

    if mocks is None and reals is not None:
        return False

    if mocks is not None and reals is None:
        return False

    if len(mocks) != len(reals):
        return False

    for mock, real in zip(mocks, reals):
        mock = elongate(mock)
        real = elongate(real)

        for mock_item, real_item in zip(mock, real):
            for key in real_item.__dict__.keys():
                mock_values = mock_item.__dict__[key]
                real_values = real_item.__dict__[key]

                mock_values = elongate(mock_values)
                real_values = elongate(real_values)

                if any([hasattr(v, '__dict__') for v in mock_values]):
                    assert_mocks_equals_objects(mock_values, real_values)
                else:
                    for mock_value, real_value in zip(mock_values,
                                                      real_values):
                        assert mock_value == real_value


def _param_or_own(param, own):
    if param is None:
        return own
    else:
        return param


# mocks
def get_score_mock(
    sets=[
        (11, 21),
        (11, 21)
    ],
    is_walkover=False
):
    score = MagicMock(spec=Score)
    score.sets = sets
    score.is_walkover = is_walkover

    return score


def get_tournament_mock(
    name=None,
    url=None,
    start_date=None,
    end_date=None,
):
    tournament = MagicMock(spec=Tournament)
    tournament.name = _param_or_own(name, 'Yonex Askim SGP 2018')
    tournament.url = _param_or_own(url, 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=889C8871-C659-4B7E-A630-325459E4EA87')  # NOQA
    tournament.start_date = _param_or_own(start_date, maya.parse('2018-04-28'))
    tournament.end_date = _param_or_own(end_date, maya.parse('2018-04-29'))

    return tournament


def get_player_mock(
    name=None,
    url=None,
    iid=None,
):
    player = MagicMock(spec=Player)
    player.name = _param_or_own(name, 'Teodor Atterström')
    # player.url = _param_or_own(url, 'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/home')  # NOQA
    player.url = _param_or_own(url, None)
    # player.iid = _param_or_own(iid, 'IID01442289')
    player.iid = _param_or_own(iid, None)

    return player


def get_match_mock(
    discipline=None,
    category=None,
    scheduled_time=None,
    team1_players=None,
    team2_players=None,
    team1_seed=None,
    team2_seed=None,
    score=None,
    duration=None,
    is_team1_winner=None,
    is_played=None
):
    match = MagicMock(spec=Match)
    match.discipline = _param_or_own(discipline, 'MS')
    match.category = _param_or_own(category, 'Elit')
    match.scheduled_time = _param_or_own(
        scheduled_time, maya.parse('2018-04-28 9:00'))
    match.team1_players = _param_or_own(
        team1_players, [get_player_mock()])
    match.team2_players = _param_or_own(
        team2_players, [get_player_mock()])
    match.team1_seed = _param_or_own(team1_seed, '1')
    match.team2_seed = _param_or_own(team2_seed, '3/4')
    match.score = _param_or_own(score, get_score_mock())
    match.duration = _param_or_own(duration, '0:46')
    match.is_team1_winner = _param_or_own(is_team1_winner, False)
    match.is_played = _param_or_own(is_played, True)

    return match


class ResponseMock(object):
    def __init__(self, html_path):
        html = self._get_html(html_path)

        self.text = html

    def _get_html(self, path):
        with open(path, 'r') as f:
            return f.read()
