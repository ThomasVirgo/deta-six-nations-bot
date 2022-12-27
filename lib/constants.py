import os

API_KEY = os.getenv("SPORT_RADAR_API_KEY")
COMPETITION_ID = "sr:competition:423"
SEASON_ID = "sr:season:92685"
BASE_URL = "http://api.sportradar.us/rugby-union/trial/v3/en"
LINEUPS_URL = f"{BASE_URL}/seasons/{SEASON_ID}/lineups.json?api_key={API_KEY}"
PROBABILITY_URL = f"{BASE_URL}/seasons/{SEASON_ID}/probabilities.json?api_key={API_KEY}"
