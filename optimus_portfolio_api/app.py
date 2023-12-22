import json
import os
from datetime import datetime

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .bookstack import BOOKSTACK_BASE_URL, BookstackClient
from .github import get_most_recent_public_project
from .utils import now_playing

MEDIA_PATH = os.getenv("MEDIA_PATH")
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")
assert MEDIA_PATH

images = os.path.join(os.path.abspath("/"), MEDIA_PATH)
app = FastAPI()

origins = ["jaydepyles.dev", "10.0.0.3", "localhost"]
# origins = ["*"]

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
    d = requests.get(f"https://api.lanyard.rest/v1/users/{DISCORD_USER_ID}").json()
    return d


@app.get("/api/github/recent")
async def get_recent_repo():
    USERNAME = "jaypyles"
    status = get_most_recent_public_project(USERNAME)
    if status:
        return json.dumps({"url": status})


@app.get("/api/bookstack/recent-page")
async def get_recent_page():
    bookstack = BookstackClient()
    pages = []
    for page in bookstack.get_pages():
        pages.append(
            {
                "url": f"{BOOKSTACK_BASE_URL}/books/{page['book_slug']}/page/{page['slug']}",
                "date": datetime.strptime(page["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            }
        )

    sorted_pages = sorted(pages, key=lambda x: x["date"])
    newest_page = sorted_pages[-1]

    response = {"url": newest_page["url"]}

    return json.dumps(response)
