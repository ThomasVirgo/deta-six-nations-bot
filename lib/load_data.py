import requests
import time
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
from lib.constants import SEASON_ID, API_KEY, BASE_URL
from lib.client import SixNationsClient


class Country(Enum):
    ENGLAND = "England"
    WALES = "Wales"
    IRELAND = "Ireland"
    SCOTLAND = "Scotland"
    ITALY = "Italy"
    FRANCE = "France"
    UNKNOWN = ""


class Endpoints:
    def __init__(self, season_id: str = SEASON_ID, api_key: str = API_KEY) -> None:
        self.season_id = season_id
        self.api_key = api_key

    @property
    def lineups_url(self):
        return (
            f"{BASE_URL}/seasons/{self.season_id}/lineups.json?api_key={self.api_key}"
        )

    @property
    def probabilities_url(self):
        return f"{BASE_URL}/seasons/{self.season_id}/probabilities.json?api_key={self.api_key}"


@dataclass
class Player:
    jersey_number: int
    is_sub: bool
    name: Optional[str] = None
    price: Optional[float] = None
    club: Optional[str] = None


@dataclass
class ClientPlayer:
    position: str
    price: str
    starting_status: str
    club: str
    name: str


@dataclass
class Team:
    id: str
    name: Country
    qualifier: str
    players: Optional[List[Player]] = None
    probability_of_winning: Optional[float] = None
    all_players: Optional[List[ClientPlayer]] = None


@dataclass
class LineUp:
    id: str
    start_time: datetime
    competition_name: str
    competitors: List[Team]
    round: Optional[int] = None


class DataLoader:
    def __init__(self, season_id: str = SEASON_ID, api_key: str = API_KEY) -> None:
        self.season_id = season_id
        self.api_key = api_key
        self.endpoints = Endpoints(self.season_id, self.api_key)
        self.lineups_dict: Dict = self.get_lineups()
        self.lineups_data: List[Dict] = self.lineups_dict.get("lineups", {})
        time.sleep(0.8)
        self.probs_dict: Dict = self.get_probablities()
        self.probs_data: List[Dict] = self.probs_dict.get(
            "sport_event_probabilities", {}
        )
        self.lineups: List[LineUp] = []
        self.extract_data()
        self.join_probabilities_data()

    def get_lineups(self):
        resp = requests.get(self.endpoints.lineups_url)
        return resp.json()

    def get_probablities(self):
        response = requests.get(self.endpoints.probabilities_url)
        return response.json()

    def extract_data(self):
        for lineup in self.lineups_data:
            sport_event: Dict = lineup.get("sport_event", {})
            id = sport_event.get("id", 0)
            start_time = sport_event.get(
                "start_time", "1800-01-01T15:00:00+00:00"
            ).split("+")[0]
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
            sport_event_context: Dict = sport_event.get("sport_event_context", {})
            comp_name = sport_event_context.get("competition", {}).get("name", "")
            round = sport_event_context.get("round", {}).get("number", None)
            competitors = sport_event.get("competitors", [])
            teams = []
            for c in competitors:
                team = Team(
                    c.get("id", ""),
                    Country(c.get("name", "")),
                    c.get("qualifier", ""),
                    self.load_players(),
                )
                teams.append(team)
            new_lineup = LineUp(id, start_time, comp_name, teams, round)
            self.lineups.append(new_lineup)

    def find_item_in_list_of_dicts(self, lst: List, key, value):
        for item in lst:
            if item[key] == value:
                return item

    def join_probabilities_data(self):
        for item in self.probs_data:
            sport_event = item.get("sport_event", {})
            id = sport_event.get("id")
            outcomes = item.get("markets", {})[0].get("outcomes")
            home_win_prob = self.find_item_in_list_of_dicts(
                outcomes, "name", "home_team_winner"
            ).get("probability")
            away_win_prob = self.find_item_in_list_of_dicts(
                outcomes, "name", "away_team_winner"
            ).get("probability")
            for lineup in self.lineups:
                if lineup.id == id:
                    for team in lineup.competitors:
                        if team.qualifier == "home":
                            team.probability_of_winning = home_win_prob
                        if team.qualifier == "away":
                            team.probability_of_winning = away_win_prob

    def load_players(self) -> List[Player]:
        # TODO
        return []

    def to_dict(self):
        lineups = [asdict(l) for l in self.lineups]
        return {"lineups": lineups}


POSITION_ID_TO_POSITION = {
    6: "back three",
    7: "centre",
    8: "fly half",
    9: "scrum half",
    10: "back row",
    11: "second row",
    12: "prop",
    13: "hooker",
}


class ClientDataLoader:
    def __init__(self, token) -> None:
        self.client = SixNationsClient(token)
        self.raw_data = self.client.get_players(page_size=500)
        self.player_data_list: LineUp[Dict] = self.raw_data.get("joueurs")
        self.players: List[Player] = []

    def create_players(self):
        for player_data in self.player_data_list:
            name = player_data.get("nomcomplet")
            club = player_data.get("club")
            position = POSITION_ID_TO_POSITION.get(player_data.get("id_position"))
            price = player_data.get("valeur")
            starting_status = player_data.get("formeprev", {}).get("tooltip")
            new_player = ClientPlayer(
                position=position,
                name=name,
                club=club,
                price=price,
                starting_status=starting_status,
            )
            self.players.append(new_player)
