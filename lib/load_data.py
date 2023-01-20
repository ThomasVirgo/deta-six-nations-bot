import requests
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
from lib.constants import SEASON_ID, API_KEY, BASE_URL


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
    name: str
    jersey_number: int


@dataclass
class Team:
    id: str
    name: str
    qualifier: str
    players: Optional[List[Player]] = None


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
        time.sleep(0.3)
        self.probs_dict: Dict = self.get_probablities()
        self.lineups_data: List[Dict] = self.lineups_dict.get("lineups", {})
        self.lineups: List[LineUp] = []
        self.extract_data()

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
                    c.get("name", ""),
                    c.get("qualifier", ""),
                    self.load_players(),
                )
                teams.append(team)
            new_lineup = LineUp(id, start_time, comp_name, teams, round)
            self.lineups.append(new_lineup)

    def load_players(self) -> List[Player]:
        # TODO
        return []

    def to_dict(self):
        lineups = [asdict(l) for l in self.lineups]
        return {"lineups": lineups}
