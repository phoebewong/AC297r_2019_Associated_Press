import pandas as pd
from src import constants
from src.api_helper import article_id_extractor
import json
import requests
import configparser

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
