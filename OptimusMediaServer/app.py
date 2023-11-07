import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

load_dotenv()
images = os.path.join(os.path.abspath("/"), os.getenv("MEDIA_PATH"))  # type: ignore

app = FastAPI()

origins = ["*"]

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
