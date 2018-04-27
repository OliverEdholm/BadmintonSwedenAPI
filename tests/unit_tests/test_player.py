# imports
from utils import ResponseMock

from badmintonswedenapi.player import get_unplayed_tournaments

import pytest
import maya


# tests
@pytest.mark.parametrize(
    'player_url, date, mock_paths, expected_urls, expected',
    [
        (
            'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/',  # NOQA
            maya.parse('2017-06-28'),
            {
                'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/tournaments?Year=2018': \  # NOQA
                    'tests/unit_tests/mocks/teodor/2018.html',
                'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/tournaments?Year=2017': \  # NOQA
                    'tests/unit_tests/mocks/teodor/2017.html',
            },
            {
                2018: 'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/tournaments?Year=2018',  # NOQA
                2017: 'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/tournaments?Year=2017',  # NOQA
            },
            [
                {
                    'name': 'Baker Tillyspelen 2018 Sollentuna',
                    'start_date': maya.parse('2018-04-28'),
                    'end_date': maya.parse('2018-04-29'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=433363A4-9D60-4FBA-B86E-F9B9CAE0D6CB'  # NOQA
                },
                {
                    'name': 'Gothenburg Open 2018',
                    'start_date': maya.parse('2018-05-11'),
                    'end_date': maya.parse('2018-05-13'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=F9DC3162-4A46-451C-AB0C-744F5D7CCD41'  # NOQA
                }
            ]
        ),
        (
            'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID00876487/',  # NOQA
            maya.parse('2018-04-28'),
            {
                'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID00876487/tournaments?Year=2018': \  # NOQA
                    'tests/unit_tests/mocks/filip/2018.html'
            },
            {
                2018: 'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID00876487/tournaments?Year=2018',  # NOQA
            },
            [
                {
                    'name': 'Yonex Askim SGP 2018',
                    'start_date': maya.parse('2018-04-28'),
                    'end_date': maya.parse('2018-04-29'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=889C8871-C659-4B7E-A630-325459E4EA87'  # NOQA
                },
            ]
        )
    ]
)
def test_get_unplayed_tournaments(player_url, date, mock_paths, expected_urls,
                                  expected, mocker):
    def side_effect(value):
        current_year = maya.now().year
        expected_url = expected_urls[current_year]

        if value == expected_url:
            return ResponseMock(mock_paths[value])
        else:
            raise Exception('Invalid URL: {value}, expected: '
                            '{expected}'.format(value=value,
                                                expected=expected_url))

    mocker.patch(
        'maya.now',
        return_value=date
    )

    mocker.patch(
        'requests.get',
        return_value=side_effect)
    )

    results = get_unplayed_tournaments(player_url)

    assert results == expected
