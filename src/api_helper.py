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
    subset = data[['id', 'headline']]
    captions = []
    for id in ids:
        try:
            caption = subset[subset['id'] == id]['headline'].values[0]
        except:
            caption = 'No Caption'
        captions.append(caption)
    return captions

def tagging_api_existing(title, body):
    """
    Tags articles (at the moment it gets tags from the dataset)
    """
    id = article_id_extractor(title, body)
    if id == None:
        return None

    art_sub = pd.read_csv(constants.CLEAN_DIR / 'article_subject.csv')
    art_person = pd.read_csv(constants.CLEAN_DIR / 'article_person.csv')
    art_place = pd.read_csv(constants.CLEAN_DIR / 'article_place.csv')
    art_org = pd.read_csv(constants.CLEAN_DIR / 'article_org.csv')

    art_sub['type'] = 'subject'
    art_person['type'] = 'person'
    art_place['type'] = 'place'
    art_org['type'] = 'org'

    art_sub = art_sub[art_sub['id'] == id][['subject_tag', 'type']].dropna(axis=0)
    art_sub = art_sub.rename(columns={"subject_tag": "tag"})

    art_person = art_person[art_person['id'] == id][['person_tag', 'type']].dropna(axis=0)
    art_person = art_person.rename(columns={"person_tag": "tag"})

    art_place = art_place[art_place['id'] == id][['place_tag', 'type']].dropna(axis=0)
    art_place = art_place.rename(columns={"place_tag": "tag"})

    art_org = art_org[art_org['id'] == id][['org_tag', 'type']].dropna(axis=0)
    art_org = art_org.rename(columns={"org_tag": "tag"})

    art_alltags = pd.concat([art_sub, art_person, art_place, art_org])

    return id, art_alltags['tag'].values, art_alltags['type'].values

def tagging_api_new(title, body):
    """
    Tags articles using API call
    """
    # retrieve password
    config = configparser.ConfigParser()
    config.read(constants.SRC_DIR / 'password.ini')
    apikey = config['key']['apikey']

    #format request to tagging api
    datasets = ['subject', 'geography', 'organization', 'person']
    request_url = f'http://cv.ap.org/annotations?apikey={apikey}'
    data = {"meta": {
                "features": [
                    {"name": "ap",
                    "authorities": datasets}],
                    "accept": "application/ld+json"},
                    "document": body,
                    "document_contenttype": "text/plain"}
    response = requests.post(url = request_url, json = data)
    if response.status_code == 200:
        json_data = response.json()
        # some tags seem to be blank, ignore if no annotation field
        if not json_data['annotation']:
            return []
        json_data = json.loads(json_data['annotation'])
        tags = []
        types = []
        # current method extracts annotation
        # if there is a type field labeled http://www.w3.org/2004/02/skos/core#Concept
        # seems to be a relevant tag
        # otherwise seems to be a category of tag e.g. Subject
        for j in json_data:
            try:
                if j['@type'][0] == 'http://www.w3.org/2004/02/skos/core#Concept':
                    tags.append(j['http://www.w3.org/2004/02/skos/core#prefLabel'][0]['@value'])
                    type = j['http://cv.ap.org/ns#authority'][0]['@value']
                    type = type.split()[1].strip().lower() # gets Subject from e.g. AP Subject
                    if type == 'geography':
                        type = 'place'
                    types.append(type)
            except:
                pass
        return tags, types
    else:
        return response.status_code

def matching_articles(ids):
    """
    Matching articles and getting headlines
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

def postprocess(x):
    """
    Post-processes output of models so we can predict images (using indices)
    """
    csv_file = constants.CLEAN_DIR / 'image_person.csv'
    data = pd.read_csv(csv_file)
    indices = [idx%len(data) for idx in x.flatten()]
    return np.array(data.iloc[indices].id).reshape(-1,1)

if __name__ == '__main__':
    text =  "Georgia Tech’s schedule to this point has been light, with a season-opener against Tennessee the hardest test to this" \
    " point. Miami (4-0, 2-0) is looking for its first 10-game win streak since 2003-04. If it is looking for inspiration, Georgia Tech can look to" \
" 2015, when it stunned ninth-ranked Florida State on a last-second blocked field goal return for a 78-yard touchdown. FSU entered that" \
" game with a 29-game win streak over ACC opponents. Miami has beaten its last six ACC foes. Georgia Tech ranks 31st in points" \
" (36.5), 35th in yards per play (6.35) and unsurprisingly, second nationally in rushing yards per game (396.0). The Yellow Jackets" \
" average 5.91 yards per carry (10th), which ranks behind Miami’s 6.40, which is sixth. Georgia Tech hasn’t finished behind Miami — or" \
" anywhere outside the top 20 — in rushing yards per carry since at least 2008.Quarterback TaQuon Marshall, a converted running back" \
" (current running back, really, in Paul Johnson‘s offense), has been a capable leader"
    print(tagging_api_new("title", text))
