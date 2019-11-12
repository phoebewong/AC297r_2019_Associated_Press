import os
import logging
import pickle
import dill
from src import api_helper
import numpy as np

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
    with open('static/models/knn_model.pkl', 'rb') as f:
        models['knn_model'] = dill.load(f)
    with open('static/models/knn_model_place.pkl', 'rb') as f:
        models['knn_model_place'] = dill.load(f)

class ArticleInput(BaseModel):
    title: str = None
    body: str


@app.post("/match")
async def new_matches(article_input: ArticleInput):
    logger.debug("trying to find good images for article: %s", article_input.title)

    # get tags
    id, tags, tag_types = api_helper.tagging_api(article_input.title, article_input.body)
    true_images = api_helper.article_images(id)

    # tags = ['general news', 'police', 'law enforcement agencies', 'government and politics',
    #         'robbery', 'theft', 'crime', 'automotive accidents', 'transportation accidents',
    #         'accidents', 'accidents and disasters', 'transportation']

    # make a prediction with the random model
    # data = [[np.random.randint(0,75000)] for i in range(20)]
    # prediction = models['random_model'].predict(data)
    # pp_preds = api_helper.postprocess(prediction).flatten()

    # make a prediction with the knn model
    article_ids, prediction = models['knn_model_place'].predict(tags)

    # get matching articles
    articles = api_helper.matching_articles(article_ids)

    pp_preds = prediction.keys()

    return {
        "status": "ok",
        "data": {
            "tags": [{"name": tag, "type": tag_types[i], "score": 0.4} for i, tag in enumerate(tags)],
            "images": [{"id": id} for id in pp_preds],
            "articles": [{"headline": headline} for headline in articles],
            "true_images": [{"id": id} for id in true_images]
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
