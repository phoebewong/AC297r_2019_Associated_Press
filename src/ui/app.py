import os
import logging

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
debug = os.environ.get("DEBUG", False)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ArticleInput(BaseModel):
    title: str = None
    body: str


@app.post("/match")
async def new_matches(article_input: ArticleInput):
    logger.debug("trying to find good images for article: %s", article_input)
    # TODO: do something with article.body ...
    return {
        "status": "ok",
        "data": {
            "tags": [
                {"name": "Sports", "score": 0.99},
                {"name": "Basketball", "score": 0.91},
                {"name": "Boston Celtics", "score": 0.2}
            ],
            "images": [
                {"id": '0b5caa00d2a34db8a7d7c4bc30e6081b', "score": 0.95},
                {"id": '0b40eeb8cff64ac3a3fae568a748dd04', "score": 0.81},
                {"id": '0b328f5537d14be4bbe800ced89b5eec', "score": 0.55},
            ]
        },
    }


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def startup_event():
    logger.info("started")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
