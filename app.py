from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

# Read data from JSON file
with open("data/data.json", "r") as f:
    data = json.load(f)

seasons_data = data["seasons"]
cast_data = data["cast"]

# Data Models
class Episode(BaseModel):
    episode_number: int
    title: str
    description: str


class Season(BaseModel):
    season_number: int
    episodes: List[Episode]


class CastMember(BaseModel):
    name: str
    role: str


app = FastAPI()

@app.get("/seasons/", response_model=List[Season])
async def get_all_seasons():
    return seasons_data

@app.get("/seasons/{season_number}/", response_model=Season)
async def get_season_by_number(season_number: int):
    for season in seasons_data:
        if season["season_number"] == season_number:
            return season
    raise HTTPException(status_code=404, detail="Season not found")

@app.get("/seasons/{season_number}/episodes/", response_model=List[Episode])
async def get_episodes_by_season(season_number: int):
    for season in seasons_data:
        if season["season_number"] == season_number:
            return season["episodes"]
    raise HTTPException(status_code=404, detail="Season not found")

@app.get("/episodes/{episode_number}/", response_model=Episode)
async def get_episode_by_number(episode_number: int):
    for season in seasons_data:
        for episode in season["episodes"]:
            if episode["episode_number"] == episode_number:
                return episode
    raise HTTPException(status_code=404, detail="Episode not found")

@app.get("/cast/", response_model=List[CastMember])
async def get_cast():
    return cast_data