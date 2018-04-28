# imports
from badmintonswedenapi.player import get_non_played_tournaments

import pytest


# tests
@pytest.mark.parametrize('url', [
    'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01384033/',  # NOQA
    'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID04055438/',  # NOQA
    'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/',  # NOQA
])
def test_search_player(url):
    results = get_non_played_tournaments(url)

    assert results is not None
