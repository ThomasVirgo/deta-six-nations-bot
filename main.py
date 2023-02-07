import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from lib.client import SixNationsClient
from lib.load_data import DataLoader, Endpoints, ClientDataLoader
from lib.logic import SelectTeam
from dataclasses import asdict
from pydantic import BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginData(BaseModel):
    email: str
    password: str


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
def all_players(request: Request):
    try:
        token = request.headers.get("token", "")
        data_loader = ClientDataLoader(token)
        data_loader.create_players()
        return [asdict(player) for player in data_loader.players]
    except Exception as e:
        return {"error", str(e)}


@app.get("/bot/client/select_players/{round}")
def all_players(request: Request, round: int):
    try:
        token = request.headers.get("token", "")
        data_loader = ClientDataLoader(token)
        data_loader.create_players()
        data_loader_2 = DataLoader()
        selector = SelectTeam(data_loader_2.lineups, round)
        teams = selector.select()
        for team in teams:
            for player in data_loader.players:
                if team.name.value == player.club:
                    if team.all_players is None:
                        team.all_players = []
                    team.all_players.append(player)
        return [asdict(team) for team in teams]
    except Exception as e:
        return {"error", str(e)}


@app.post("/bot/login")
def login(login_data: LoginData):
    try:
        client = SixNationsClient()
        token = client.login(login_data.email, login_data.password)
        return token
    except Exception as e:
        return {"error", str(e)}
