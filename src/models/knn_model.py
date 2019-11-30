import pandas as pd
import numpy as np
from src import constants
import os
import csv
import json

# KNN model
class KNN():
    # @param k: number of neighbors to return
    def __init__(self):
        self.get_article_to_image()
        self.get_train_csv()

    def get_article_to_image(self):
        df = pd.read_csv(constants.CLEAN_DIR / 'image_summary.csv')
        g = df.groupby("article_idx")['id']
        self.article_to_image = g.apply(list).to_dict()

    def get_train_csv(self):
        try:
            self.train = pd.read_csv(constants.DATA_DIR / 'knn_tags.csv')
        except FileNotFoundError:
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

            train = pd.DataFrame({'id':train.index, 'tags':train.values})
            train.to_csv(constants.DATA_DIR / 'knn_tags.csv', header=True)
            self.train = train

    # returns number of normalized exact tag overlap
    def baseline_score(self,t0,t1):
        return len(set(t0) & set(t1))/len(set(t0).union(set(t1)))

    # @param sim: function to return similarity score
    # @param test: article to predict in form (id, tags)
    # TODO: implement sep functions for text train and image train
    def predict(self, test_tags, true_id=None, k=4):
        ranks = {}
        train = self.train.copy()
        train_ids, train_tags_all = train['id'].values, train['tags'].values
        test_tags = [t.lower().replace('"',"") for t in test_tags]
        if true_id is not None:
            k = k + 1 # eliminating the true article

        # go through ids
        for ind in range(len(train_ids)):
            train_id, train_tags = train_ids[ind], train_tags_all[ind][2:-2].replace("'", "").split(',')
            train_tags = [t.strip() for t in train_tags]
            s = self.baseline_score(train_tags, test_tags)
            if len(ranks) < k:
                ranks[len(ranks)] = (train_id, s)
            elif s > min(ranks.values(), key=lambda x:x[1])[1]:
                key = min(ranks.keys(), key=lambda x:ranks[x][1])
                ranks[key] = (train_id, s)
        ranks = sorted(ranks.values(), key = lambda x:x[1], reverse=True)

        # map to predicted images
        article_ids = []
        pred_imgs = []
        scores = []
        for article_id, score in ranks:
            if article_id == true_id:
                continue
            img_ids = self.article_to_image[str(article_id)]
            for img_id in img_ids:
                if img_id in pred_imgs:
                    continue
                pred_imgs.append(img_id)
                scores.append(score)
            article_ids.append(article_id)
        return article_ids, pred_imgs, scores

if __name__ == '__main__':
    knn = KNN()
    test_tags = ['bernie sanders', 'hillary clinton', 'jackie cilley', 'presidential elections', 'campaigns',
                 'elizabeth warren', 'government and politics', 'sherrod brown', 'political endorsements', 'elections',
                 'state elections', 'united states presidential election', 'u.s. democratic party', 'nan', 'national elections',
                 'kamala harris', 'kirsten gillibrand', 'social issues']
    article_ids, pred_imgs, scores = knn.predict(test_tags)
    print(pred_imgs)
