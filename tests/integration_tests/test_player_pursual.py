# imports
from badmintonswedenapi.search import search_player

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

    non_played_tournaments = player.get_non_played_tournaments()

    assert non_played_tournaments is not None
