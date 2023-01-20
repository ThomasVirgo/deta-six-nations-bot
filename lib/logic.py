from typing import List, Optional
from lib.load_data import LineUp, Player, Team

JERSEY_ORDERING = [
    [
        11,
        14,
        10,
        2,
    ],
    [
        13,
        1,
        4,
        15,
    ],
    [
        12,
        3,
        5,
        9,
    ],
    [
        11,
        14,
        8,
        7,
    ],
    [
        16,
        6,
    ],
]


class SelectTeam:
    def __init__(self, lineups: List[LineUp], round: int) -> None:
        def round_filter(lineup: LineUp):
            if lineup.round == round:
                return True
            return False

        self.selected_lineup: Optional[List[Player]] = None
        self.lineups = list(filter(round_filter, lineups))

    def rank_teams(self) -> List[Team]:
        teams = []

        def key(x: Team):
            return x.probability_of_winning

        for lineup in self.lineups:
            for team in lineup.competitors:
                teams.append(team)
        return sorted(teams, key=key, reverse=True)

    def select(self):
        teams_ranked = self.rank_teams()
        for i, jersey_number_group in enumerate(JERSEY_ORDERING):
            team = teams_ranked[i]
            for jersey_number in jersey_number_group:
                is_sub = (i == 3 and jersey_number in [11, 14]) or jersey_number == 16
                team.players.append(Player(jersey_number, is_sub))
        return teams_ranked[:5]
