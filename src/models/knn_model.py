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
        self.tag_ref = {'org':'org_tag', 'person':'person_tag', 'place':'place_tag', 'subject':'subject_tag'}
        self.article_feat_csvs = ['article_person.csv','article_org.csv','article_place.csv','article_subject.csv']
        self.image_feat_csvs = ['image_person.csv','image_org.csv','image_place.csv','image_subject.csv']
        self.get_train_csv()

    def get_train_csv(self):
        """
        Get/create the files used for the kNN model
        """
        try:
            self.train_article = pd.read_csv(constants.DATA_DIR / 'knn_article_tags.csv')
        except FileNotFoundError:
            train = pd.Series([])
            for csv_file in os.listdir(constants.CLEAN_DIR):
                if csv_file in self.article_feat_csvs:
                    df = pd.read_csv(constants.CLEAN_DIR / csv_file)
                    feat = csv_file[8:-4]
                    g = df.dropna(axis=0).groupby("id")[self.tag_ref[feat]]
                    if train.empty:
                        train = g.apply(lambda x: list(x.astype(str).str.lower()))
                    else:
                        g = g.apply(lambda x: list(x.astype(str).str.lower()))
                        train = train.combine(g, lambda x1, x2: list(set(x1+x2)), fill_value=[])

            train = pd.DataFrame({'id':train.index, 'tags':train.values})
            train.to_csv(constants.DATA_DIR / 'knn_article_tags.csv', header=True)
            self.train_article = train

        try:
            self.train_image = pd.read_csv(constants.DATA_DIR / 'knn_image_tags.csv')
        except FileNotFoundError:
            train = pd.Series([])
            for csv_file in os.listdir(constants.CLEAN_DIR):
                if csv_file in self.image_feat_csvs:
                    df = pd.read_csv(constants.CLEAN_DIR / csv_file)
                    feat = csv_file[6:-4]
                    g = df.dropna(axis=0).groupby("id")[self.tag_ref[feat]]
                    if train.empty:
                        train = g.apply(lambda x: list(x.astype(str).str.lower()))
                    else:
                        g = g.apply(lambda x: list(x.astype(str).str.lower()))
                        train = train.combine(g, lambda x1, x2: list(set(x1+x2)), fill_value=[])

            train = pd.DataFrame({'id':train.index, 'tags':train.values})
            train.to_csv(constants.DATA_DIR / 'knn_image_tags.csv', header=True)
            self.train_image = train

    def baseline_score(self,t0,t1):
        """
        returns number of normalized exact tag overlap
        """
        return len(set(t0) & set(t1))/len(set(t0).union(set(t1)))

    def predict_articles(self, test_tags, true_id=None, k=4):
        """
        Function to predict top matching articles
        @param sim: function to return similarity score
        @param test: article to predict in form (id, tags)
        @param true_id: if the article being used is an actual
        @param k: number of articles to look for
        """
        ranks = {}
        train = self.train_article.copy()
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

        article_ids, scores = [], []
        for article_id, score in ranks:
            if article_id == true_id:
                continue
            article_ids.append(article_id)
            scores.append(score)
        return article_ids, scores

    def predict_images(self, test_tags, k=4):
        """
        Function to predict top matching articles
        @param sim: function to return similarity score
        @param test: article to predict in form (id, tags)
        @param k: number of images to look for
        """
        ranks = {}
        train = self.train_image.copy()
        train_ids, train_tags_all = train['id'].values, train['tags'].values
        test_tags = [t.lower().replace('"',"") for t in test_tags]

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

        image_ids, scores = [], []
        for image_id, score in ranks:
            image_ids.append(image_id)
            scores.append(score)
        return image_ids, scores

if __name__ == '__main__':
    knn = KNN()
    test_tags = ['bernie sanders', 'hillary clinton', 'jackie cilley', 'presidential elections', 'campaigns',
                 'elizabeth warren', 'government and politics', 'sherrod brown', 'political endorsements', 'elections',
                 'state elections', 'united states presidential election', 'u.s. democratic party', 'national elections',
                 'kamala harris', 'kirsten gillibrand', 'social issues']
    article_ids, scores = knn.predict_articles(test_tags)
    image_ids, scores = knn.predict_images(test_tags)
    print(image_ids, article_ids)
