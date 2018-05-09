# imports
from .utils import get_player_mock
from .utils import get_score_mock

from badmintonswedenapi.match import Score
from badmintonswedenapi.match import Match

import pytest
import maya


# tests
class TestScore(object):
    @pytest.mark.parametrize('score_data', [
        {
            'sets': [
                (11, 21),
                (11, 21)
            ]
        },
        {
            'sets': [],
            'is_walkover': True
        }
    ])
    def test_init(self, score_data):
        score = Score(**score_data)

        assert score.sets is not None
        assert score.is_walkover is not None


class TestMatch(object):
    def get_example_match(
        self,
        discipline='MS',
        category='Elit',
        scheduled_time=maya.parse('2018-04-28 9:00'),
        team1_players=[
            get_player_mock()
        ],
        team2_players=[
            get_player_mock()
        ],
        team1_seed='1',
        team2_seed='3/4',
        score=get_score_mock(),
        duration='0:46',
        is_team1_winner=False,
        is_played=True
    ):
        match = Match(
            discipline=discipline,
            category=category,
            scheduled_time=scheduled_time,
            team1_players=team1_players,
            team2_players=team2_players,
            team1_seed=team1_seed,
            team2_seed=team2_seed,
            score=score,
            duration=duration,
            is_team1_winner=is_team1_winner,
            is_played=is_played
        )

        return match
