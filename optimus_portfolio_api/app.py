import json
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from optimus_portfolio_api.github import get_most_recent_public_project
from optimus_portfolio_api.utils import now_playing

load_dotenv()
MEDIA_PATH = os.getenv("MEDIA_PATH")
USER_ID = os.getenv("USER_ID")
if MEDIA_PATH:
    images = os.path.join(os.path.abspath("/"), MEDIA_PATH)  # type: ignore
app = FastAPI()

origins = ["jaydepyles.dev", "10.0.0.3", "localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def try_image_path(image_path: str) -> str | None:
    """Try and check for image extensions extensions"""
    path = os.path.join(images, image_path)

    if os.path.exists(path):
        return path

    return None


@app.get("/api/images/{image_file}")
async def get_image(image_file: str):
    if path := try_image_path(image_file):
        return FileResponse(path, media_type="image/jpeg")
    else:
        return {"error": "Image not found"}


@app.get("/api/spotify/now-playing")
async def get_playing():
    return json.dumps(now_playing())


@app.get("/api/discord/status")
async def get_status():
    d = requests.get(f"https://api.lanyard.rest/v1/users/{USER_ID}").json()
    return d


@app.get("/api/github/recent")
async def get_recent_repo():
    USERNAME = "jaypyles"
    status = get_most_recent_public_project(USERNAME)
    if status:
        return json.dumps({"url": status})
