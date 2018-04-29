# imports
from badmintonswedenapi.search import search_player

import pytest


# tests
@pytest.mark.parametrize('query', [
    'wqfgoqwdgdfgdfg',
    'Åberg',
    'Teodor Atterström',
    'Klara Blomquist'
])
def test_search_player(query):
    results = search_player(query)

    assert results is not None
