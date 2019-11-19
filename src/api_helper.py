import pandas as pd
import numpy as np
import constants
import json
import requests
import configparser

def tagging_api(body):
    """
    Tags articles
    """

    #retrieve password
    config = configparser.ConfigParser()
    config.read('password.ini')
    apikey =  (config['key']['apikey'])

    #available taxonomy dataset for call
    datasets = ['subject', 'geography', 'organization', 'person']

    for data in datasets:
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
            if not json_data['annotation']:
                return []
            json_data = json.loads(json_data['annotation'])
            tags = []
            for j in json_data:
                try:
                    if j['@type'][0] == 'http://www.w3.org/2004/02/skos/core#Concept':
                        tags.append(j['http://www.w3.org/2004/02/skos/core#prefLabel'][0]['@value'])
                except:
                    pass
            return tags
        else:
            return response.status_code

def matching_articles(ids):
    """
    Matching articles and getting headlines
    """
    csv_file = constants.hOUTPUT_CSV_DIR / 'article_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'eadline']].dropna(axis=0)
    headlines = []
    for id in ids:
        try:
            headlines.append(subset[subset['id'] == id]['headline'].values[0])
        except:
            continue
    return headlines

def postprocess(x):
    """
    Post-processes output of models so we can predict images (using indices)
    """
    csv_file = constants.OUTPUT_CSV_DIR / 'image_person.csv'
    data = pd.read_csv(csv_file)
    indices = [idx%len(data) for idx in x.flatten()]
    return np.array(data.iloc[indices].id).reshape(-1,1)

if __name__ == '__main__':
    # ids = ['0141bc4aee7c4352a242a8138135f9be', '00d713a2b6cb44c88fbd2fd3f10228f3', '00c6682106da42f299ab9955de385aa5']
    # print(matching_articles(ids))
    text =  "Georgia Tech’s schedule to this point has been light, with a season-opener against Tennessee the hardest test to this" \
    " point. Miami (4-0, 2-0) is looking for its first 10-game win streak since 2003-04. If it is looking for inspiration, Georgia Tech can look to" \
" 2015, when it stunned ninth-ranked Florida State on a last-second blocked field goal return for a 78-yard touchdown. FSU entered that" \
" game with a 29-game win streak over ACC opponents. Miami has beaten its last six ACC foes. Georgia Tech ranks 31st in points" \
" (36.5), 35th in yards per play (6.35) and unsurprisingly, second nationally in rushing yards per game (396.0). The Yellow Jackets" \
" average 5.91 yards per carry (10th), which ranks behind Miami’s 6.40, which is sixth. Georgia Tech hasn’t finished behind Miami — or" \
" anywhere outside the top 20 — in rushing yards per carry since at least 2008.Quarterback TaQuon Marshall, a converted running back" \
" (current running back, really, in Paul Johnson‘s offense), has been a capable leader"
    print(tagging_api(text))
