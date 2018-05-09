# imports
from .utils import ResponseMock
from .utils import get_match_mock
from .utils import get_player_mock
from .utils import get_score_mock
from .utils import assert_mocks_equals_objects

from badmintonswedenapi.tournament import Tournament

import maya


# tests
class TestTournament(object):
    def get_example_tournament(
        self,
        name='Yonex Askim SGP 2018',
        url='http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=889C8871-C659-4B7E-A630-325459E4EA87',  # NOQA
        start_date=maya.parse('2018-04-28'),
        end_date=maya.parse('2018-04-29')
    ):
        tournament = Tournament(
            name=name,
            url=url,  # NOQA
            start_date=start_date,
            end_date=end_date
        )

        return tournament

    def test_init(self):
        tournament = self.get_example_tournament()

        assert tournament.name is not None
        assert tournament.url is not None
        assert tournament.start_date is not None
        assert tournament.end_date is not None

    def test_get_all_matches(self, mocker):
        def side_effect(value):
            expected_urls = [
                'http://badmintonsweden.tournamentsoftware.com/sport/matches.aspx?id=889C8871-C659-4B7E-A630-325459E4EA87&d=20180428',  # NOQA
                'http://badmintonsweden.tournamentsoftware.com/sport/matches.aspx?id=889C8871-C659-4B7E-A630-325459E4EA87&d=20180429'  # NOQA
            ]
            if value in expected_urls:
                date = value.split('&d=')[1]

                mock_path = 'tests/unit_tests/mocks/tournament/{}.html'.format(
                    date)
                return ResponseMock(mock_path)
            else:
                raise Exception('Invalid URL: {value}, expected: '
                                '{expected}'.format(value=value,
                                                    expected=expected_urls))

        mocker.patch(
            'requests.get',
            side_effect=side_effect
        )

        tournament = self.get_example_tournament()

        matches = tournament.get_all_matches()

        mocks = []
        to_test = []

        # men singles
        to_test.append(matches[8])
        mocks.append(get_match_mock(
            discipline='MS',
            category='Elit',
            scheduled_time=maya.parse('2018-04-28 9:30'),
            team1_players=[get_player_mock(name='Simon Sandholm')],
            team2_players=[get_player_mock(name='Emil Johansson')],
            team1_seed='',
            team2_seed='',
            score=get_score_mock(sets=[(21, 16), (21, 11)]),
            duration='0:36',
            is_team1_winner=True,
            is_played=True
        ))

        # women singles
        to_test.append(matches[19])
        mocks.append(get_match_mock(
            discipline='WS',
            category='Elit',
            scheduled_time=maya.parse('2018-04-28 10:00'),
            team1_players=[get_player_mock(name='Jennie Carlsson')],
            team2_players=[get_player_mock(name='Lovisa Johansson')],
            team1_seed='',
            team2_seed='',
            score=get_score_mock(sets=[(21, 17), (21, 14)]),
            duration='0:33',
            is_team1_winner=True,
            is_played=True
        ))

        # men doubles
        to_test.append(matches[25])
        mocks.append(get_match_mock(
            discipline='MD',
            category='Elit',
            scheduled_time=maya.parse('2018-04-28 10:00'),
            team1_players=[
                get_player_mock(name='Mattias Borg'),
                get_player_mock(name='Mikael Westerbäck')
            ],
            team2_players=[
                get_player_mock(name='Simon Sandholm'),
                get_player_mock(name='Hannes Svensson')
            ],
            team1_seed='',
            team2_seed='',
            score=get_score_mock(sets=[(21, 8), (21, 18)]),
            duration='0:37',
            is_team1_winner=True,
            is_played=True
        ))

        # women doubles
        to_test.append(matches[31])
        mocks.append(get_match_mock(
            discipline='WD',
            category='Elit',
            scheduled_time=maya.parse('2018-04-28 10:30'),
            team1_players=[
                get_player_mock(name='Lydia Demetriades'),
                get_player_mock(name='Malena Norrman')
            ],
            team2_players=[
                get_player_mock(name='Madeleine Persson'),
                get_player_mock(name='Stina Runesson')
            ],
            team1_seed='',
            team2_seed='',
            score=get_score_mock(sets=[(21, 14), (21, 13)]),
            duration='0:29',
            is_team1_winner=True,
            is_played=True
        ))

        # mixed doubles
        # first match
        to_test.append(matches[0])
        mocks.append(get_match_mock(
            discipline='XD',
            category='Elit',
            scheduled_time=maya.parse('2018-04-28 9:00'),
            team1_players=[
                get_player_mock(name='Marcus Jansson'),
                get_player_mock(name='Cecilia Närfors')
            ],
            team2_players=[
                get_player_mock(name='Jacob Lundskog'),
                get_player_mock(name='Astrid Svensson')
            ],
            team1_seed='',
            team2_seed='',
            score=get_score_mock(sets=[(21, 14), (21, 19)]),
            duration='0:50',
            is_team1_winner=True,
            is_played=True
        ))

        # walkover
        to_test.append(matches[32])
        mocks.append(get_match_mock(
            discipline='WD',
            category='Elit',
            scheduled_time=maya.parse('2018-04-28 10:30'),
            team1_players=[
                get_player_mock(name='Salisa Chayruksa'),
                get_player_mock(name='Rebecca Johnsson')
            ],
            team2_players=[
                get_player_mock(name='Moa Sjöö'),
                get_player_mock(name='Edith Urell')
            ],
            team1_seed='',
            team2_seed='',
            score=get_score_mock(sets=[], is_walkover=True),
            duration='',
            is_team1_winner=True,
            is_played=True
        ))

        # injury during match
        to_test.append(matches[45])
        mocks.append(get_match_mock(
            discipline='MS',
            category='Elit',
            scheduled_time=maya.parse('2018-04-28 11:30'),
            team1_players=[
                get_player_mock(name='Nils Ihse'),
            ],
            team2_players=[
                get_player_mock(name='Joel Hansson'),
            ],
            team1_seed='',
            team2_seed='',
            score=get_score_mock(sets=[(21, 17), (9, 2)], is_walkover=False),
            duration='0:23',
            is_team1_winner=True,
            is_played=True
        ))

        # match with seeded player
        to_test.append(matches[38])
        mocks.append(get_match_mock(
            discipline='MS',
            category='Elit',
            scheduled_time=maya.parse('2018-04-28 11:00'),
            team1_players=[
                get_player_mock(name='Andy Tsai'),
            ],
            team2_players=[
                get_player_mock(name='Jesper De Waal'),
            ],
            team1_seed='1',
            team2_seed='',
            score=get_score_mock(sets=[(21, 15), (21, 9)]),
            duration='0:36',
            is_team1_winner=True,
            is_played=True
        ))

        # last match
        to_test.append(matches[-1])
        mocks.append(get_match_mock(
            discipline='WD',
            category='Elit',
            scheduled_time=maya.parse('2018-04-29 14:00'),
            team1_players=[
                get_player_mock(name='Berfin Aslan'),
                get_player_mock(name='Iben Bergstein'),
            ],
            team2_players=[
                get_player_mock(name='Klara Johansson'),
                get_player_mock(name='Olivia Wänglund'),
            ],
            team1_seed='1',
            team2_seed='2',
            score=get_score_mock(sets=[(21, 17), (21, 16)]),
            duration='',
            is_team1_winner=True,
            is_played=True
        ))

        # a match
        to_test.append(matches[62])
        mocks.append(get_match_mock(
            discipline='MS',
            category='A',
            scheduled_time=maya.parse('2018-04-28 12:00'),
            team1_players=[
                get_player_mock(name='Calle Badenfors'),
            ],
            team2_players=[
                get_player_mock(name='Krittaphat Thiapwacha'),
            ],
            team1_seed='1',
            team2_seed='',
            score=get_score_mock(sets=[(21, 12), (21, 15)]),
            duration='0:28',
            is_team1_winner=True,
            is_played=True
        ))

        assert_mocks_equals_objects(mocks, to_test)

    def test_get_all_matches_non_played(self, mocker):
        def side_effect(value):
            expected_url = 'http://badmintonsweden.tournamentsoftware.com/sport/matches.aspx?id=55DA6622-FF9B-4E89-ADC4-13FCF07A839C&d=20180505'  # NOQA

            if value == expected_url:
                mock_path = 'tests/unit_tests/mocks/tournament/' \
                            'non_played_matches.html'
                return ResponseMock(mock_path)
            else:
                raise Exception('Invalid URL: {value}, expected: '
                                '{expected}'.format(value=value,
                                                    expected=expected_url))

        mocker.patch(
            'requests.get',
            side_effect=side_effect
        )

        tournament = self.get_example_tournament(
            name='Advania Spåret Open Ungdom 2018',
            url='http://badmintonsweden.tournamentsoftware.com/sport/tournament.aspx?id=55DA6622-FF9B-4E89-ADC4-13FCF07A839C',  # NOQA
            start_date=maya.parse('2018-05-05'),
            end_date=maya.parse('2018-05-05'),
        )

        matches = tournament.get_all_matches()

        mocks = []
        to_test = []

        # men singles
        to_test.append(matches[0])
        mocks.append(get_match_mock(
            discipline='MS',
            category='U11',
            scheduled_time=maya.parse('2018-05-05 9:00'),
            team1_players=[get_player_mock(name='Leo Hyltner')],
            team2_players=[get_player_mock(name='Mike Dong')],
            team1_seed='',
            team2_seed='',
            score=get_score_mock(sets=[]),
            duration='',
            is_team1_winner=True,   # doesn't really matter
            is_played=False
        ))

        assert_mocks_equals_objects(mocks, to_test)
