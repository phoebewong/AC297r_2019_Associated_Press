import os
import logging
from src import api_helper
from src.models import t2i_recsys
from src.models.avg_embeddings_model import AvgEmbeddings
import numpy as np
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

class InputParams(BaseModel):
    title: str = None
    body: str
    model: str


@app.post("/match")
async def new_matches(input_params: InputParams):
    logger.debug("trying to find good images for article: %s", input_params.title)
    logger.debug("model used: %s", input_params.model)

    # get tags
    title, body, model = input_params.title, input_params.body, input_params.model

    id = api_helper.article_id_extractor(title, body)
    if id == None:
        id, title, body = api_helper.random_article_extractor()

    id, tags, tag_types = api_helper.tagging_api(title, body)

    true_images = api_helper.article_images(id)
    true_captions = api_helper.image_captions(true_images)

    # get matching articles
    # articles = api_helper.matching_articles(article_ids)

    textrank_entities, textrank_score, entities_list = extract_textrank_from_text(body, tagging_API_entities = tags)

    # t2t model stuff
    if model == 't2t':
        t2i_object = t2i_recsys.T2I(id, entities_list.copy(), list(textrank_score))
        predicted_imgs = t2i_object.predict(4)
        pred_captions = api_helper.image_captions(predicted_imgs)
        articles = {None}

    elif model == 'emb':
        predicted_imgs = embed_model.predict_images(title, k=8)
        pred_captions = api_helper.image_captions(predicted_imgs)
        articles = {None}

    return {
        "status": "ok",
        "data": {
            "tags": [{"name": tag, "type": tag_types[list(tags).index(tag)], "score": textrank_score[i]} for i, tag in enumerate(entities_list)],
            "images": [{"id": id, "caption": pred_captions[i]} for i,id in enumerate(predicted_imgs)],
            "articles": [articles],
            "true_images": [{"id": id, "caption": true_captions[i]} for i, id in enumerate(true_images)]
        },
    }


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def startup_event():
    global embed_model
    embed_model = AvgEmbeddings(300)
    logger.info("started")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
