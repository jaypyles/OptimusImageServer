import os

from bson import ObjectId
from fastapi import APIRouter, Response
from gridfs import GridFS
from pymongo import MongoClient

mongo_router = APIRouter()


def format_date_with_suffix(date):
    day = date.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    return date.strftime(f"%B {day}{suffix}, %Y")


@mongo_router.get("/api/post_images/{image_id}")
async def get_image(image_id: str):
    client = MongoClient(
        f"mongodb://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@uploader-mongo:27017/"
    )
    db = client["posts"]
    fs = GridFS(db)

    print(image_id)

    grid_out = fs.get(ObjectId(image_id))

    print(grid_out)

    return Response(content=grid_out.read(), media_type="image/jpeg")


@mongo_router.get("/api/posts")
async def get_posts():
    client = MongoClient(
        f"mongodb://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@uploader-mongo:27017/"
    )

    db = client["posts"]
    posts = db["posts"]

    documents = list()
    for document in posts.find()[:25]:  # TODO: implement loading type logic
        print(document)
        image_id: ObjectId = document["image_id"]

        documents.append(
            {
                "image_id": str(image_id),
                "description": document["description"],
                "time_posted": format_date_with_suffix(document["dateUploaded"]),
            }
        )

    return {"posts": documents}
