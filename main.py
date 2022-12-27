import requests
from fastapi import FastAPI
from lib.logic import Endpoints

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
        endpoints = Endpoints()
    else:
        endpoints = Endpoints(season_id)
    try:
        resp = requests.get(endpoints.lineups_url)
        data = resp.json()
    except:
        return {"error": "unable to make request to sport radar"}
    return data


@app.get("/bot/probabilities/{season_id}")
def probabilities(season_id: str):
    if season_id == "default":
        endpoints = Endpoints()
    else:
        endpoints = Endpoints(season_id)
    try:
        resp = requests.get(endpoints.probabilities_url)
        data = resp.json()
    except:
        return {"error": "unable to make request to sport radar"}
    return data
