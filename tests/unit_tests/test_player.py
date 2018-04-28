# imports
from utils import ResponseMock

from badmintonswedenapi.player import get_non_played_tournaments

import pytest
import maya


# tests
@pytest.mark.parametrize(
    'player_url, date, mock_paths, expected_urls, expected',
    [
        (
            'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/',  # NOQA
            maya.parse('2017-12-20'),
            {
                'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/tournaments/?Year=2018': 'tests/unit_tests/mocks/player/teodor/2018.html',  # NOQA
                'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/tournaments/?Year=2017': 'tests/unit_tests/mocks/player/teodor/2017.html',  # NOQA
            },
            [
                'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/tournaments/?Year=2018',  # NOQA
                'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID01442289/tournaments/?Year=2017',  # NOQA
            ],
            [
                {
                    'name': 'Gothenburg Open 2018',
                    'start_date': maya.parse('2018-05-11'),
                    'end_date': maya.parse('2018-05-13'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=F9DC3162-4A46-451C-AB0C-744F5D7CCD41'  # NOQA
                },
                {
                    'name': 'Baker Tillyspelen 2018 Sollentuna',
                    'start_date': maya.parse('2018-04-28'),
                    'end_date': maya.parse('2018-04-29'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=433363A4-9D60-4FBA-B86E-F9B9CAE0D6CB'  # NOQA
                },
                {
                    'name': 'Botkyrkaslaget 2018',
                    'start_date': maya.parse('2018-04-14'),
                    'end_date': maya.parse('2018-04-15'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=A32AD161-7740-4402-AE5B-3E320A891FBF'  # NOQA
                },
                {
                    'name': 'Skogås Open 2018',
                    'start_date': maya.parse('2018-03-24'),
                    'end_date': maya.parse('2018-03-25'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=E69D9AD0-0C58-487C-AC40-C221F22910F9'  # NOQA
                },
                {
                    'name': 'SM U17 2018',
                    'start_date': maya.parse('2018-03-16'),
                    'end_date': maya.parse('2018-03-18'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=80EF0E31-B0B6-4EE5-BEC6-41887882AE4A'  # NOQA
                },
                {
                    'name': 'Storslaget 2018',
                    'start_date': maya.parse('2018-02-03'),
                    'end_date': maya.parse('2018-02-04'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=503A08AA-7738-4D37-ADD8-7BAF09000989'  # NOQA
                },
                {
                    'name': 'Elon InfraCity Open',
                    'start_date': maya.parse('2018-01-27'),
                    'end_date': maya.parse('2018-01-28'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=0573D6D2-5EF0-4E28-86EE-E9DD589F7F71'  # NOQA
                },
                {
                    'name': 'SJT U17 + Elit U19 Borlänge 2018',
                    'start_date': maya.parse('2018-01-13'),
                    'end_date': maya.parse('2018-01-14'),
                    'url': 'http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=5F9895B4-5DE4-4F32-9CE7-E726F3F39E64'  # NOQA
                }
            ]
        ),
        (
            'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID00876487/',  # NOQA
            maya.parse('2018-04-28'),
            {
                'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID00876487/tournaments/?Year=2018': 'tests/unit_tests/mocks/player/filip/2018.html'  # NOQA
            },
            [
                'http://badmintonsweden.tournamentsoftware.com/player/3C3E88CA-FA0B-43B0-81E3-C5A8BC84F0EF/IID00876487/tournaments/?Year=2018',  # NOQA
            ],
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
def test_get_non_played_tournaments(player_url, date, mock_paths,
                                    expected_urls, expected, mocker):
    def side_effect(value):
        if value in expected_urls:
            return ResponseMock(mock_paths[value])
        else:
            raise Exception('Invalid URL: {value}, expected: '
                            '{expected}'.format(value=value,
                                                expected=expected_urls))

    mocker.patch(
        'maya.now',
        return_value=date
    )

    mocker.patch(
        'requests.get',
        side_effect=side_effect
    )

    results = get_non_played_tournaments(player_url)

    assert results == expected
