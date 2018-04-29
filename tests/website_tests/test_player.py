# imports
from badmintonswedenapi.player import Player

import pytest


# tests
@pytest.mark.parametrize('player', [
    Player(
        name='Filip Karlborg',
        url='http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID00876487/',  # NOQA
        iid='IID00876487'
    ),
    Player(
        name='Teodor Atterström',
        url='http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/',  # NOQA
        iid='IID01442289'
    )
])
def test_search_player(player):
    results = player.get_non_played_tournaments()

    assert results is not None
