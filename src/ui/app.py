# general imports
import os
import logging
import numpy as np
import pandas as pd
import time

# models
from src.models import t2i_recsys
from src.models.avg_embeddings_model import AvgEmbeddings
from src.models.soft_cosine_model import SoftCosine
from src.models.knn_model import KNN
from src.models.USE_model import USE_Recsys
from src.nlp_util.textacy_util import extract_textrank_from_text

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
                    'knn': 'k-Nearest Neighbor Model',
                    'use': 'Universal Sentence Embedding Model'}

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

    ids = []
    true_imgs_list = []
    knn_preds_list = []
    t2t_preds_list = []
    softcos_preds_list = []
    emb_preds_list = []
    use_preds_list = []

    for i in range(500):
        print(f'{i}: {time.time() - start_time}')
        # get tags
        title, body, model, slider = input_params.title, input_params.body, input_params.model, input_params.slider/2.5
        num = input_params.num

        num_arts = 2 if model == 'all' else 4
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
            # true_captions, true_summaries = api_helper.image_captions(true_images)
            true_tags = api_helper.image_tags(true_images)
            ids.append(id)
            true_imgs_list.append(true_images)

        textrank_entities, textrank_score, entities_list = extract_textrank_from_text(body, tagging_API_entities = tags)
        tag_time = time.time() - start_time

        predicted_imgs = []
        predicted_arts = []
        model_names = []
        model_times = {}

        # exact tag based models
        num_imgs = 60
        # num_imgs = int((4-slider) * num/8) if model == 'all' else num

        model_start_time = time.time()
        if model == 't2t' or model == 'all' and num_imgs > 0:
            t2i_object = t2i_recsys.T2I(id, entities_list.copy(), list(textrank_score))
            pred_imgs = t2i_object.predict(num_imgs)
            predicted_imgs.extend(pred_imgs)
            t2t_preds_list.append(pred_imgs)
            model_names.extend(['t2t']*num_imgs)
            model_times['t2t'] = time.time() - model_start_time
            model_start_time = time.time()


        if model == 'knn' or model == 'all' and num_imgs > 0:
            pred_imgs, scores = knn_model.predict_images(tags, k=num_imgs)
            article_ids, scores = knn_model.predict_articles(tags, true_id=id, k=num_arts)
            # predicted_arts.extend(article_ids)
            predicted_imgs.extend(pred_imgs)
            knn_preds_list.append(pred_imgs)
            model_names.extend(['knn']*num_imgs)
            model_times['knn'] = time.time() - model_start_time
            model_start_time = time.time()

        # semantically related models
        # num_imgs = int(slider * num/12) if model == 'all' else num

        if model == 'emb' or model == 'all' and num_imgs > 0:
            pred_imgs = embed_model.predict_images(title, k=num_imgs)
            predicted_imgs.extend(pred_imgs)
            # predicted_arts.extend(embed_model.predict_articles(title, k=num_arts, true_id=id))
            emb_preds_list.append(pred_imgs)
            model_names.extend(['emb']*num_imgs)
            model_times['emb'] = time.time() - model_start_time
            model_start_time = time.time()

        if model == 'softcos' or model == 'all' and num_imgs > 0:
            pred_imgs = soft_cosine_model.predict(title, art_id=id, tags=tags, num_best=num_imgs)
            predicted_imgs.extend(pred_imgs)
            softcos_preds_list.append(pred_imgs)
            model_names.extend(['softcos']*num_imgs)
            model_times['softcos'] = time.time() - model_start_time
            model_start_time = time.time()

        if model == 'use' or model == 'all' and num_imgs > 0:
            place_tags = [tags[i] for i in range(len(tags)) if tag_types[i] == 'place']
            pred_imgs = USE_model.predict(title, article_id=id, article_tags=place_tags, output_size=num_imgs)
            use_preds_list.append(pred_imgs)
            predicted_imgs.extend(pred_imgs)
            model_names.extend(['use']*num_imgs)
            model_times['use'] = time.time() - model_start_time

        # pred_captions, pred_summaries = api_helper.image_captions(predicted_imgs)
        # articles = api_helper.article_headlines(predicted_arts)
        # image_tags = api_helper.image_tags(predicted_imgs)

        img_time = time.time() - start_time - tag_time

    df_dict = {'ids': ids, 'true_imgs': true_imgs_list, 'knn': knn_preds_list, 't2t': t2t_preds_list,
               'softcos': softcos_preds_list, 'emb': emb_preds_list, 'use': use_preds_list}
    df = pd.DataFrame(df_dict)
    df.to_csv('data.csv')

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
            'model_times': model_times,
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
    global embed_model, knn_model, soft_cosine_model, USE_model
    embed_model = AvgEmbeddings(50)
    soft_cosine_model = SoftCosine()
    knn_model = KNN()
    USE_model = USE_Recsys()
    logger.info('started')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
