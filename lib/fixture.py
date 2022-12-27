from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Player:
    name: str
    jersey_number: int


@dataclass
class Team:
    name: str
    players: Optional[List[Player]] = None


@dataclass
class Fixture:
    date_str: str
    home_team: Team
    away_team: Team
    home_team_win_prob: float
    away_team_win_pron: float
