from lib.constants import BASE_URL, API_KEY
from lib.constants import SEASON_ID


class Endpoints:
    def __init__(self, season_id: str = SEASON_ID) -> None:
        self.season_id = season_id

    @property
    def lineups_url(self):
        return f"{BASE_URL}/seasons/{self.season_id}/lineups.json?api_key={API_KEY}"

    @property
    def probabilities_url(self):
        return (
            f"{BASE_URL}/seasons/{self.season_id}/probabilities.json?api_key={API_KEY}"
        )
