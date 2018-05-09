# classes
class Score(object):
    def __init__(self, sets=[], is_walkover=False):
        self.sets = sets
        self.is_walkover = is_walkover


class Match(object):
    def __init__(
        self,
        discipline=None,  # remove
        category=None,  # remove
        scheduled_time=None,
        team1_players=None,
        team2_players=None,
        team1_seed=None,
        team2_seed=None,
        score=None,
        duration=None,  # remove
        is_team1_winner=None,  # remove
        is_played=True
    ):
        self.discipline = discipline
        self.category = category
        self.scheduled_time = scheduled_time
        self.team1_players = team1_players
        self.team2_players = team2_players
        self.team1_seed = team1_seed
        self.team2_seed = team2_seed
        self.score = score
        self.duration = duration
        self.is_team1_winner = is_team1_winner
        self.is_played = is_played
