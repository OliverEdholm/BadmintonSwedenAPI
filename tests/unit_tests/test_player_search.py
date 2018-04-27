# imports
from utils import ResponseMock

from badmintonswedenapi.player_search import search_player

import pytest


# tests
@pytest.mark.parametrize('query, mock_path, expected_url, expected',
[
    (
        'Oliver Edholm',
        'tests/unit_tests/mocks/player_search/oliver.html',
        'http://badmintonsweden.tournamentsoftware.com/find/player?q=Oliver Edholm',  # NOQA
        [
            {
                'name': 'Oliver Edholm',
                'url': 'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID00792657/',  # NOQA
                'iid': 'IID00792657'
            }
        ]
    ),
    (
        'Teodor Atterström',
        'tests/unit_tests/mocks/player_search/teodor.html',
        'http://badmintonsweden.tournamentsoftware.com/find/player?q=Teodor Atterström',  # NOQA
        [
            {
                'name': 'Teodor Atterström',
                'url': 'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/',  # NOQA
                'iid': 'IID01442289'
            }
        ]
    )
])
def test_search_player(query, mock_path, expected_url, expected, mocker):
    def side_effect(value):
        if value == expected_url:
            return ResponseMock(mock_path)
        else:
            raise Exception('Invalid URL: {value}, expected: '
                            '{expected_url}'.format(value=value,
                                                    expected=expected_url))

    mocker.patch(
        'requests.get',
        side_effect=side_effect
    )

    results = search_player(query)

    assert results == expected
