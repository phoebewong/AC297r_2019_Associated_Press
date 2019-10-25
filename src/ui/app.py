import os
import logging
import pickle
from src import api_helper

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

models = {}

def load_models():
    global models
    with open('static/models/random_model.pkl', 'rb') as f:
        models['random_model'] = pickle.load(f)


class ArticleInput(BaseModel):
    title: str = None
    body: str


@app.post("/match")
async def new_matches(article_input: ArticleInput):
    logger.debug("trying to find good images for article: %s", article_input)

    # get tags
    tags = api_helper.tagging_api(article_input.title, article_input.body)

    # make a prediction with the model
    data = [[len(article_input.title)], [len(article_input.body)], [len(article_input.body.split(' '))]]
    prediction = models['random_model'].predict(data)
    pp_preds = api_helper.postprocess(prediction).flatten()

    return {
        "status": "ok",
        "data": {
            "tags": [{"name": tag} for tag in tags],
            "images": [{"id": id} for id in pp_preds]
        },
    }


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def startup_event():
    load_models()
    logger.info("started")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
