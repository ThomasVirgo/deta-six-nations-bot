from fastapi import FastAPI

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
def read_item(season_id: str):
    return {"season_id": season_id}


@app.get("/bot/probabilities/{season_id}")
def read_item(season_id: str):
    return {"season_id": season_id}
