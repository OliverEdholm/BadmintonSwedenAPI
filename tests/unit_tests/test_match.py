# # imports
# from utils import PlayerMock
#
# from badmintonswedenapi.match import Match
# from badmintonswedenapi.match import Score
#
# import pytest
#
# import maya
#
#
# # helpers
# def get_example_match(
#         discipline='MS',
#         category='Elit',
#         scheduled_time=maya.parse('2018-04-28 9:00'),
#         team1_players=[
#             PlayerMock()
#         ],
#         team2_players=[
#             PlayerMock()
#         ],
#         team1_seed='1',
#         team2_seed='3/4',
#         score=[
#             (11, 21),
#             (15, 21)
#         ],
#         duration='0:46',
#         is_team1_winner=False):
#     match = Match(
#         discipline=discipline,
#         category=category,
#         scheduled_time=scheduled_time,
#         team1_players=team1_players,
#         team2_players=team2_players,
#         team1_seed=team1_seed,
#         team2_seed=team2_seed,
#         score=score,
#         duration=duration,
#         is_team1_winner=is_team1_winner
#     )
#
#     return match
#
#
# # tests
# @pytest.mark.parametrize('score', [
#     Score(
#         sets=[
#             (11, 21),
#             (11, 21)
#         ]
#     ),
#     Score(
#         sets=[],
#         is_walkover=True
#     )
# ])
# def test_score(score):
#     assert score.score is not None
#     assert score.is_walkover is not None
#
#
# @pytest.mark.parametrize('match', [
#     get_example_match(discipline='MS'),
#     get_example_match(discipline='WS'),
#     get_example_match(discipline='MD'),
#     get_example_match(discipline='WD'),
#     get_example_match(discipline='XD'),
# ])
# def test_match(match):
#     assert match.discipline is not None
#     assert match.category is not None
#     assert match.scheduled_time is not None
#     assert match.team1_players is not None
#     assert match.team2_players is not None
#     assert match.team1_seed is not None
#     assert match.team2_seed is not None
#     assert match.score is not None
#     assert match.duration is not None
#
#
# def test_match_incorrect_discipline():
#     with pytest.raises(AssertionError):
#         get_example_match(discipline='XS')
