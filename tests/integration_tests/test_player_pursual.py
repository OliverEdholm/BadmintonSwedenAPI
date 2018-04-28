# imports
from badmintonswedenapi.player_search import search_player
from badmintonswedenapi.player import get_non_played_tournaments

import pytest


# tests
@pytest.mark.parametrize('query', [
    'Oliver',
    'Jacob',
    'Sara'
])
def test_player_pursual(query):
    players = search_player(query)
    player = players[0]

    non_played_tournaments = get_non_played_tournaments(player['url'])

    assert non_played_tournaments is not None
