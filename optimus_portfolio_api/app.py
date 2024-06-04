# STL
import os
from typing import Any  # type: ignore[reportAny]
from datetime import datetime

# PDM
import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# LOCAL
from optimus_portfolio_api.utils import now_playing
from optimus_portfolio_api.github import get_most_recent_public_project
from optimus_portfolio_api.bookstack import BookstackClient
from optimus_portfolio_api.mongo.MongoRouter import mongo_router

MEDIA_PATH: str = os.environ["MEDIA_PATH"]
DISCORD_USER_ID: str = os.environ["DISCORD_USER_ID"]
NOTION_SECRET: str = os.environ["NOTION_SECRET"]
WIKI_URL: str = os.environ["WIKI_URL"]

ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png"}
images: str = os.path.join(os.path.abspath("/"), MEDIA_PATH)
app: FastAPI = FastAPI()
app.include_router(router=mongo_router)

origins: list[str] = ["jaydepyles.dev", "10.0.0.6", "localhost"]
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
    path: str = os.path.join(images, image_path)

    if os.path.exists(path):
        return path

    return None


@app.get(path="/api/images/{image_file}", response_model=None)
async def get_image(image_file: str) -> FileResponse | JSONResponse:
    if path := try_image_path(image_path=image_file):
        _, file_extension = os.path.splitext(image_file)
        if file_extension.lower() in ALLOWED_EXTENSIONS:
            return FileResponse(path, media_type="image/jpeg")
        else:
            return JSONResponse({"error": "Invalid image file format"})
    else:
        return JSONResponse({"error": "Image not found"})


@app.get(path="/api/spotify/now-playing")
async def get_playing() -> JSONResponse:
    return JSONResponse(content=now_playing())


@app.get(path="/api/discord/status")
async def get_status() -> dict[str, Any]:
    d: dict[str, Any] = requests.get(
        url=f"https://api.lanyard.rest/v1/users/{DISCORD_USER_ID}"
    ).json()
    return d


@app.get(path="/api/github/recent")
async def get_recent_repo() -> JSONResponse:
    USERNAME = "jaypyles"
    status: str | None = get_most_recent_public_project(username=USERNAME)

    if not status:
        return JSONResponse(content={"url": ""})

    return JSONResponse(content={"url": status})


@app.get(path="/api/bookstack/recent-page")
async def get_recent_page() -> JSONResponse:
    bookstack: BookstackClient = BookstackClient()
    pages: list[dict[str, str | datetime]] = []
    for page in bookstack.get_pages():
        updated_at: str = page["updated_at"]
        pages.append(
            {
                "url": f"{WIKI_URL}/books/{page['book_slug']}/page/{page['slug']}",
                "date": datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
            }
        )

    sorted_pages = sorted(pages, key=lambda x: x["date"])
    newest_page = sorted_pages[-1]

    response = {"url": newest_page["url"]}

    return JSONResponse(content=response)
