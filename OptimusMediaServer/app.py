import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

load_dotenv()
images = os.path.join(os.path.abspath("/"), os.getenv("MEDIA_PATH"))

app = FastAPI()


@app.get("/api/images/{image_file}")
async def get_image(image_file: str):
    path = os.path.join(images, image_file)
    if os.path.exists(path):
        return FileResponse(
            path=path,
            filename=str(hash(image_file)),
            media_type="text/image",
        )
    else:
        return {"error": "Image not found"}
