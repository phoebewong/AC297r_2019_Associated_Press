import pandas as pd
import numpy as np
from src import constants
import pickle
import dill

# KNN model
class KNN():
    # @param k: number of neighbors to return
    def __init__(self, k, article_to_image):
        self.k = k
        self.article_to_image = article_to_image

    # @param train: training set of articles
    # @article_to_image: map of images associated with each article
    def fit(self, train):
        self.train = train

    # returns number of normalized exact tag overlap
    def baseline_score(self, t0,t1):
        return len(set(t0) & set(t1))/len(t0)

    # @param sim: function to return similarity score
    # @param test: article to predict in form (id, tags)
    # TODO: implement sep functions for text train and image train
    def predict(self, test):
        test_id, test_tags = test
        self.ranks = {}
        for train_id, train_tags in self.train:
            s = self.baseline_score(train_tags, test_tags)
            if len(self.ranks) < self.k:
                self.ranks[len(self.ranks)] = (train_id, s)
            elif s > min(self.ranks.values(), key=lambda x:x[1])[1]:
                key = min(self.ranks.keys(), key=lambda x:self.ranks[x][1])
                self.ranks[key] = (train_id, s)
        self.ranks = sorted(self.ranks.values(), key = lambda x:x[1], reverse=True)
        # map to predicted images
        self.pred = {}
        for train_id, s in self.ranks:
            img_ids = self.article_to_image[str(train_id)]
            for img_id in img_ids:
                self.pred[img_id] = s
        return self.pred

    def score(self):
        pass

if __name__ == '__main__':
    csv_file = constants.CLEAN_DIR / 'article_subject.csv'
    df = pd.read_csv(csv_file)
    g = df.groupby("id")["subject_tag"]
    train = g.apply(lambda x: list(x.astype(str).str.lower()))
    train = train.iteritems()

    # images associated with an article
    df = pd.read_csv(constants.CLEAN_DIR / 'image_summary.csv')
    g = df.groupby("article_idx")['id']
    article_images = g.apply(list).to_dict()

    # knn model
    model = KNN(3, article_images)
    model.fit(train)

    filename = 'knn_model.pkl'
    dill.dump(model, open(filename, 'wb'))
