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
        "data": [
            {"id": 123456, "score": 0.95},
            {"id": 987654, "score": 0.81},
            {"id": 543212, "score": 0.55},
        ],
    }


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def startup_event():
    logger.info("started")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
