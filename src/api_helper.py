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

def matching_articles(id):
    """
    Matching articles
    """
    csv_file = constants.OUTPUT_CSV_DIR / 'article_summary.csv'
    data = pd.read_csv(csv_file)
    all_headlines = data['headline'].dropna().values
    return all_headlines[np.random.randint(low=0, high=len(all_headlines), size=3)]

def postprocess(x):
    """
    Post-processes output of models so we can predict images (using indices)
    """
    csv_file = constants.OUTPUT_CSV_DIR / 'image_person.csv'
    data = pd.read_csv(csv_file)
    indices = [idx%len(data) for idx in x.flatten()]
    return np.array(data.iloc[indices].id).reshape(-1,1)
