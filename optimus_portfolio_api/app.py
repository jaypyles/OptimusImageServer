import json
import os
from datetime import datetime

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from optimus_portfolio_api.bookstack import BOOKSTACK_BASE_URL, BookstackClient
from optimus_portfolio_api.github import get_most_recent_public_project
from optimus_portfolio_api.mongo.MongoRouter import mongo_router
from optimus_portfolio_api.notion import query_dev, query_ready
from optimus_portfolio_api.utils import now_playing

MEDIA_PATH = os.getenv("MEDIA_PATH")
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")
NOTION_SECRET = os.environ["NOTION_SECRET"]
WIKI_URL = os.environ["WIKI_URL"]
assert MEDIA_PATH

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
images = os.path.join(os.path.abspath("/"), MEDIA_PATH)
app = FastAPI()
app.include_router(mongo_router)

origins = ["jaydepyles.dev", "10.0.0.6", "localhost"]
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
        _, file_extension = os.path.splitext(image_file)
        if file_extension.lower() in ALLOWED_EXTENSIONS:
            return FileResponse(path, media_type="image/jpeg")
        else:
            return {"error": "Invalid image file format"}
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
    else:
        return json.dumps({"url": ""})


@app.get("/api/bookstack/recent-page")
async def get_recent_page():
    bookstack = BookstackClient()
    pages = []
    for page in bookstack.get_pages():
        pages.append(
            {
                "url": f"{WIKI_URL}/books/{page['book_slug']}/page/{page['slug']}",
                "date": datetime.strptime(page["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            }
        )

    sorted_pages = sorted(pages, key=lambda x: x["date"])
    newest_page = sorted_pages[-1]

    response = {"url": newest_page["url"]}

    return json.dumps(response)


@app.get("/api/notion/ready")
async def get_ready_for_development():
    pages = await query_ready(NOTION_SECRET)

    return json.dumps({"data": pages})


@app.get("/api/notion/dev")
async def get_in_development():
    pages = await query_dev(NOTION_SECRET)

    return json.dumps({"data": pages})
