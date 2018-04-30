# imports
from badmintonswedenapi.player import Player
from badmintonswedenapi.player import Tournament

from mock import MagicMock

import maya
from faker import Faker

# setup
faker = Faker('sv_SE')


# helpers
def is_mock_values_equals(mocks, reals):
    if mocks is None and reals is None:
        return True

    if mocks is None and reals is not None:
        return False

    if mocks is not None and reals is None:
        return False

    if len(mocks) != len(reals):
        return False

    requirements = []
    for mock, real in zip(mocks, reals):
        requirements.append(all([mock.__dict__[key] == real.__dict__[key]
                                 for key in real.__dict__.keys()]))

    return all(requirements)


def _param_or_own(param, own):
    if param is None:
        return own
    else:
        return param


# mocks
def get_tournament_mock(
    name=None,
    url=None,
    start_date=None,
    end_date=None,
):
    tournament = MagicMock(spec=Tournament)
    tournament.name = _param_or_own(name, faker.name())
    tournament.url = _param_or_own(url, faker.url())
    tournament.start_date = _param_or_own(start_date, maya.parse(faker.date()))
    tournament.end_date = _param_or_own(end_date, maya.parse(faker.date()))

    return tournament


def get_player_mock(
    name=None,
    url=None,
    iid=None,
):
    player = MagicMock(spec=Player)
    player.name = _param_or_own(name, faker.name())
    player.url = _param_or_own(url, faker.url())
    player.iid = _param_or_own(iid, 'IID' + str(faker.random_number(8)))

    return player


class ResponseMock:
    def __init__(self, html_path):
        html = self._get_html(html_path)

        self.text = html

    def _get_html(self, path):
        with open(path, 'r') as f:
            return f.read()
