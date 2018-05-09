# imports
from badmintonswedenapi.tournament import Tournament

import pytest
import maya


# tests
@pytest.mark.parametrize('tournament', [
    Tournament(
        name='Gothenburg Open 2018',
        url='http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=F9DC3162-4A46-451C-AB0C-744F5D7CCD41',  # NOQA
        start_date=maya.parse('2018-05-11'),
        end_date=maya.parse('2018-05-13'),
    ),
    Tournament(
        name='Umeå Nordiska 2018',
        url='http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=027CB692-2488-4C63-A1B6-10A6FF05B7C3',  # NOQA
        start_date=maya.parse('2018-04-28'),
        end_date=maya.parse('2018-04-29'),
    )
])
def test_get_all_matches(tournament):
    results = tournament.get_all_matches()

    assert results is not None
