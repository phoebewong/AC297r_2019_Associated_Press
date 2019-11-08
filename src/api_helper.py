import pandas as pd
import numpy as np
from src import constants

def tagging_api(title, body, num=3):
    """
    Tags articles
    """
    csv_file = constants.OUTPUT_CSV_DIR / 'article_person.csv'
    data = pd.read_csv(csv_file)
    all_tags = data['person_tag'].dropna().values
    return all_tags[np.random.randint(low=0, high=len(all_tags), size=3)]

def matching_articles(ids):
    """
    Matching articles and getting headlines
    """
    csv_file = constants.OUTPUT_CSV_DIR / 'article_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'headline']].dropna(axis=0)
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
    ids = ['0141bc4aee7c4352a242a8138135f9be', '00d713a2b6cb44c88fbd2fd3f10228f3', '00c6682106da42f299ab9955de385aa5']
    print(matching_articles(ids))
