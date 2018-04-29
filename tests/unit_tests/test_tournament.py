# imports
from badmintonswedenapi.tournament import Tournament

import maya


# tests
def test_tournament():
    tournament = Tournament(
        name='Yonex Askim SGP 2018',
        url='http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=889C8871-C659-4B7E-A630-325459E4EA87',  # NOQA
        start_date=maya.parse('2018-04-28'),
        end_date=maya.parse('2018-04-29')
    )

    assert tournament.name is not None
    assert tournament.url is not None
    assert tournament.start_date is not None
    assert tournament.end_date is not None
