import requests
from fastapi import FastAPI
from lib.load_data import DataLoader, Endpoints, ClientDataLoader
from lib.logic import SelectTeam
from dataclasses import asdict

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Message": "Welcome to your six nations fantasy bot.",
        "Endpoints": {
            "/bot/lineups/{season_id}": "get lineups for that season id",
            "/bot/raw_probabilities/": "raw probabilities data",
            "/bot/raw_lineups/": "raw lineups data",
            "/bot/select_players/{round}": "select team for given round",
            "/bot/client/all_players": "all players from six nations site",
        },
    }


@app.get("/bot/lineups/{season_id}")
def lineups(season_id: str):
    try:
        if season_id == "default":
            data_loader = DataLoader()
        else:
            data_loader = DataLoader(season_id)
        return data_loader.to_dict()
    except Exception as e:
        return {"error", str(e)}


@app.get("/bot/raw_lineups/")
def probabilities():
    try:
        endpoints = Endpoints()
        resp = requests.get(endpoints.lineups_url)
        return resp.json()
    except Exception as e:
        return {"error", str(e)}


@app.get("/bot/raw_probabilities/")
def probabilities():
    try:
        endpoints = Endpoints()
        resp = requests.get(endpoints.probabilities_url)
        return resp.json()
    except Exception as e:
        return {"error", str(e)}


@app.get("/bot/select_players/{round}")
def probabilities(round: int):
    try:
        data_loader = DataLoader()
        selector = SelectTeam(data_loader.lineups, round)
        return [asdict(team) for team in selector.select()]
    except Exception as e:
        return {"error", str(e)}


@app.get("/bot/client/all_players")
def all_players():
    try:
        data_loader = ClientDataLoader()
        data_loader.create_players()
        return [asdict(player) for player in data_loader.players]
    except Exception as e:
        return {"error", str(e)}
