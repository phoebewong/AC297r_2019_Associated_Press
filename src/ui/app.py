import os
import logging
import pickle
import dill
from src import api_helper
from src.nlp_util.textacy_util import *

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

class ArticleInput(BaseModel):
    title: str = None
    body: str


@app.post("/match")
async def new_matches(article_input: ArticleInput):
    logger.debug("trying to find good images for article: %s", article_input)

    # get tags
    # tags = api_helper.tagging_api(article_input.title, article_input.body)
    tags = ['general news', 'police', 'law enforcement agencies', 'government and politics',
            'robbery', 'theft', 'crime', 'automotive accidents', 'transportation accidents',
            'accidents', 'accidents and disasters', 'transportation']

    # Example tags from AP tagging API from article id "0a0e0db8ae42425897b6381481663611"
    AP_tags = ['General news', 'Government and politics',
       'Funerals and memorial services', 'Recep Tayyip Erdogan',
       'Kemal Kilicdaroglu', 'Ankara', 'Turkey', 'Western Europe',
       'Europe', 'Middle East', 'Turkey government']
    tags_type = ['subject', 'subject', 'subject', 'person', 'person', 'place',
       'place', 'place', 'place', 'place', 'org']
    # make a prediction with the random model
    # data = [[len(article_input.title)], [len(article_input.body)], [len(article_input.body.split(' '))], [10] , [20], [30], [40]]
    # prediction = models['random_model'].predict(data)
    # pp_preds = api_helper.postprocess(prediction).flatten()

    # Get textrank bags of words, importance score and AP tags (that are bags of words)
    textrank_entities, textrank_score, entities_list = extract_textrank_from_text(article_input.body, tagging_API_entities = AP_tags)
    print(textrank_entities)
    print(textrank_score)
    print(entities_list)

    # make a prediction with the knn model
    data = (tags)
    article_ids, prediction = models['knn_model'].predict(data)

    # get matching articles
    articles = api_helper.matching_articles(article_ids)

    pp_preds = prediction.keys()

    return {
        "status": "ok",
        "data": {
            "tags": [{"name": tag, "score": textrank_score[ix]} for ix, tag in enumerate(entities_list)],
            "images": [{"id": id} for id in pp_preds],
            "articles": [{"headline": headline} for headline in articles],
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
