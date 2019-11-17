import pandas as pd
import numpy as np
from src import constants

# KNN model
class KNN():
    # @param k: number of neighbors to return
    def __init__(self, k):
        self.k = k
        self.article_ti_image = None

    def get_article_to_image():
        df = pd.read_csv(constants.CLEAN_DIR / 'image_summary.csv')
        g = df.groupby("article_idx")['id']
        self.article_to_image = g.apply(list).to_dict()

    # returns number of normalized exact tag overlap
    def baseline_score(self,t0,t1):
        return len(set(t0) & set(t1))/len(t0)

    # @param sim: function to return similarity score
    # @param test: article to predict in form (id, tags)
    # TODO: implement sep functions for text train and image train
    def predict(self, test_tags):
        if self.article_to_image == None:
            self.get_article_to_image()

        ranks = {}
        train = self.train.copy()
        train_ids, train_tags_all = train.index, train.values

        # go through ids
        for ind in range(len(train_ids)):
            train_id, train_tags = train_ids[ind], train_tags_all[ind]
            s = self.baseline_score(train_tags, test_tags)
            if len(ranks) < self.k:
                ranks[len(ranks)] = (train_id, s)
            elif s > min(ranks.values(), key=lambda x:x[1])[1]:
                key = min(ranks.keys(), key=lambda x:ranks[x][1])
                ranks[key] = (train_id, s)
        ranks = sorted(ranks.values(), key = lambda x:x[1], reverse=True)

        # map to predicted images
        train_ids = []
        pred = {}
        for train_id, s in ranks:
            img_ids = self.article_to_image[str(train_id)]
            for img_id in img_ids:
                pred[img_id] = s
            train_ids.append(train_id)
        return train_ids, pred

    def score(self):
        pass

if __name__ == '__main__':
    # read in article tags
    tag_ref = {'ap_category':'category_code',
           'event':'event_tag',
           'org':'org_tag',
           'org_industry':'org_industry_tag',
           'person':'person_tag',
           'person_team':'person_team_tag',
           'person_type':'person_type',
           'place':'place_tag',
           'subject':'subject_tag',
           'summary':'headline_extended'
          }

    article_feat_csvs = ['article_person.csv','article_org.csv','article_place.csv','article_subject.csv']
    train = pd.Series([])
    for csv_file in os.listdir(constants.CLEAN_DIR):
        if csv_file in article_feat_csvs:
            df = pd.read_csv(constants.CLEAN_DIR / csv_file)
            feat = csv_file[8:-4]
            g = df.groupby("id")[tag_ref[feat]]
            if train.empty:
                train = g.apply(lambda x: list(x.astype(str).str.lower()))
            else:
                g = g.apply(lambda x: list(x.astype(str).str.lower()))
                train = train.combine(g, lambda x1, x2: list(set(x1+x2)), fill_value=[])

    # images associated with an article
    df = pd.read_csv(constants.CLEAN_DIR / 'image_summary.csv')
    g = df.groupby("article_idx")['id']
    article_images = g.apply(list).to_dict()

    # knn model
    model = KNN(3)
