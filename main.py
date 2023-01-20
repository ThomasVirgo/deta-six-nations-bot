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
            "/bot/raw_probabilities/": "raw probabilities data",
            "/bot/raw_lineups/": "raw lineups data",
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
