import requests
from fastapi import FastAPI
from lib.load_data import DataLoader, Endpoints

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Message": "Welcome to your six nations fantasy bot.",
        "Endpoints": {
            "/bot/lineups/{season_id}": "get lineups for that season id",
            "/bot/probabilities/{season_id}": "get odds of winning team for that season id",
        },
    }


@app.get("/bot/lineups/{season_id}")
def lineups(season_id: str):
    if season_id == "default":
        data_loader = DataLoader()
    else:
        data_loader = DataLoader(season_id)
    return data_loader.to_dict()


@app.get("/bot/probabilities/{season_id}")
def probabilities(season_id: str):
    endpoints = Endpoints()
    resp = requests.get(endpoints.probabilities_url)
    return resp.json()
