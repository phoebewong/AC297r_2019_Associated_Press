import pandas as pd
import numpy as np
from src import constants
import json
import requests
import configparser
import time

def log_data(data):
    """
    Logs data (what images people like or dislike) in json files
    """
    json_file = constants.LOGGING_DIR / f'{int(time.time()*1000)}.json'
    with open(json_file, 'w') as f:
        json.dump(data, f)

def random_article_extractor():
    """
    Gets the text and body of a random article in our dataset
    """
    csv_file = constants.CLEAN_DIR / 'article_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'headline', 'full_text']]
    ind = np.random.choice(range(len(subset)))

    id = subset['id'].values[ind]
    title = subset['headline'].values[ind]
    body = subset['full_text'].values[ind]

    return id, title, body

def article_id_extractor(title, body):
    """
    If a title and body is in our dataset, we return its corresponding id
    """
    csv_file = constants.CLEAN_DIR / 'article_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'headline']]
    try:
        return subset[subset['headline'] == title]['id'].values[0]
    except:
        return None

def article_images(id):
    """
    Gets all the images for a particular article id
    """
    csv_file = constants.CLEAN_DIR / 'image_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'article_idx']]
    images = subset[subset['article_idx'] == id]['id'].values
    return images

def image_captions(ids):
    """
    Gets the image caption for an image
    """
    csv_file = constants.CLEAN_DIR / 'image_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'headline', 'summary']]
    captions = []
    summaries = []
    for id in ids:
        subsubset = subset[subset['id'] == id]
        try:
            caption = subsubset['headline'].values[0]
        except:
            caption = 'No Caption'
        captions.append(caption)

        try:
            summary = subsubset['summary'].values[0]
        except:
            caption = 'No Summary'
        summaries.append(summary)
    return captions, summaries

def image_tags(ids):
    """
    Gets the image tags for a list of image ids
    """
    csv_file = constants.DATA_DIR / 'knn_image_tags.csv'
    data = pd.read_csv(csv_file)
    all_tags = []
    for id in ids:
        subset = data[data['id'] == id]
        try:
            tags = subset['tags'].values[0].replace('[','').replace(']','').strip().split(',')
        except:
            tags = []
        all_tags.append(tags)
    return all_tags

def article_headlines(ids):
    """
    Getting headlines for a set of headlines
    """
    csv_file = constants.CLEAN_DIR / 'article_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'headline']].dropna(axis=0)
    headlines = []
    for id in ids:
        try:
            headlines.append({'id': id, 'headline': subset[subset['id'] == id]['headline'].values[0]})
        except:
            headlines.append({'id': id, 'headline': 'no headline found: {}'.format(id)})

    return headlines
