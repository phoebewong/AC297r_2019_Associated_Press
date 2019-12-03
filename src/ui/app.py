# general imports
import os
import logging
import numpy as np
import time

# models
from src.models import t2i_recsys
from src.models.avg_embeddings_model import AvgEmbeddings
from src.models.soft_cosine_model import SoftCosine
from src.models.knn_model import KNN
from src.nlp_util.textacy_util import *

# API and UI files
from src import api_helper
from src import tagging_api
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
debug = os.environ.get('DEBUG', False)

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

model_names_dict = {'t2t': 'Tag-to-tag Model',
                    'emb': 'Embedding Model',
                    'softcos': 'Soft Cosine Model',
                    'knn': 'k-Nearest Neighbor Model'}

class InputParams(BaseModel):
    title: str
    body: str
    model: str
    slider: float
    num: int
    images: list = []
    id: str = None

@app.post('/match')
async def new_matches(input_params: InputParams):
    start_time = time.time()
    logger.debug('trying to find good images for article: %s', input_params.title)
    logger.debug('model used: %s', input_params.model)

    # get tags
    title, body, model, slider = input_params.title, input_params.body, input_params.model, input_params.slider
    num = input_params.num

    if model == 'all':
        num_per_model = int(num/4)
        num_arts = 2
    else:
        num_per_model = num
        num_arts = 4

    true_images, true_captions, true_summaries, true_tags = [], [], [], []

    id = api_helper.article_id_extractor(title, body)

    # no article text or body
    if len(title) == 0 and len(body) == 0:
        id, title, body = api_helper.random_article_extractor()
        print(f'Missing title and/or body. Using a random article instead')

    # new article
    if id == None:
        print(f'New article not in dataset')
        print(f'Title: {title}')
        tags, tag_types = tagging_api.tagging_api_new(title, body)
        print(tags, tag_types)

    # existing article
    else:
        print(f'Article id:{id}, title: {title}')
        id, tags, tag_types = tagging_api.tagging_api_existing(title, body)
        true_images = api_helper.article_images(id)
        true_captions, true_summaries = api_helper.image_captions(true_images)
        true_tags = api_helper.image_tags(true_images)

    textrank_entities, textrank_score, entities_list = extract_textrank_from_text(body, tagging_API_entities = tags)
    tag_time = time.time() - start_time

    predicted_imgs = []
    predicted_arts = []
    model_names = []

    # Multiplier based on slider value
    # 0: t2t and knn (2), softcos and emb (0)
    # 2.5: t2t and knn (1.5), softcos and emb (0.5)
    # 5: t2t and knn (1), softcos and emb (1)
    # 7.5: t2t & knn (0.5), softcos and emb (1.5)
    # 10: t2t & knn (0), softcos and emb (2)

    multiplier = (10-slider)/5.0
    num_imgs = int(multiplier*num_per_model) if model == 'all' else num_per_model

    # exact tag based models
    if model == 't2t' or model == 'all' and num_imgs > 0:
        t2i_object = t2i_recsys.T2I(id, entities_list.copy(), list(textrank_score))
        predicted_imgs.extend(t2i_object.predict(num_imgs))
        model_names.extend(['t2t']*num_imgs)

    if model == 'knn' or model == 'all' and num_imgs > 0:
        img_ids, scores = knn_model.predict_images(tags, k=num_imgs)
        article_ids, scores = knn_model.predict_articles(tags, true_id=id, k=num_arts)
        predicted_arts.extend(article_ids)
        predicted_imgs.extend(img_ids)
        model_names.extend(['knn']*num_imgs)

    # reseting multiplier for semantically related models
    multiplier = slider/5.0
    num_imgs = int(multiplier*num_per_model) if model == 'all' else num_per_model

    # semantically related models
    if model == 'emb' or model == 'all' and num_imgs > 0:
        predicted_imgs.extend(embed_model.predict_images(title, k=num_imgs))
        predicted_arts.extend(embed_model.predict_articles(title, k=num_arts, true_id=id))
        model_names.extend(['emb']*num_imgs)

    if model == 'softcos' or model == 'all' and num_imgs > 0:
        predicted_imgs.extend(soft_cosine_model.predict(title, art_id=id, tags=tags, num_best=num_imgs))
        model_names.extend(['softcos']*num_imgs)

    pred_captions, pred_summaries = api_helper.image_captions(predicted_imgs)
    articles = api_helper.article_headlines(predicted_arts)
    image_tags = api_helper.image_tags(predicted_imgs)

    img_time = time.time() - start_time - tag_time

    return {
        'status': 'ok',
        'data': {
            'id': id,
            'title': title,
            'body': body,
            'tags': [{'name': tag,
                      'type': tag_types[list(tags).index(tag)],
                      'score': textrank_score[i]
                      } for i, tag in enumerate(entities_list)],
            'images': [{'id': id,
                        'caption': pred_captions[i],
                        'summary': pred_summaries[i],
                        'tags': image_tags[i],
                        'model': model_names_dict[model_names[i]],
                        'liked': False,
                        'disliked': False
                        } for i,id in enumerate(predicted_imgs)],
            'articles': articles,
            'true_images': [{'id': id,
                             'caption': true_captions[i],
                             'summary': true_summaries[i],
                             'tags': true_tags[i],
                             } for i, id in enumerate(true_images)],
            'time': {'tag_time': f'{tag_time:0.2f} seconds', 'img_time': f'{img_time:0.2f} seconds'}
        },
    }

@app.post('/log')
async def log_data(input_params: InputParams):
    print('logging data')
    title, body, model = input_params.title, input_params.body, input_params.model
    id, images, slider = input_params.id, input_params.images, input_params.slider
    num = input_params.num

    api_helper.log_data({'title': title, 'body': body, 'model': model, 'id': id, 'images': images, 'slider': slider, 'num': num})

    return {
        'status': 'ok'
    }

@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.on_event('startup')
async def startup_event():
    global embed_model, knn_model, soft_cosine_model
    embed_model = AvgEmbeddings(50)
    soft_cosine_model = SoftCosine()
    knn_model = KNN()
    logger.info('started')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
