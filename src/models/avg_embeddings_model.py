from src import constants
import numpy as np
import pandas as pd
import csv
import json

class AvgEmbeddings:
    "class function for tag-to-image recommendation"
    def __init__(self, D):
        # dimension of embeddings to use
        self.D = D

        # get words dictionary
        self.get_words_dict()

        # data
        self.article_summary = pd.read_csv(f'{constants.CLEAN_DIR}/{constants.Text_Prefix}summary.csv')
        self.image_summary =  pd.read_csv(f'{constants.CLEAN_DIR}/{constants.Media_Prefix}summary.csv')

        # get embeddings
        self.get_embedding_files()

    def get_words_dict(self):
        """
        Get a dictionary of words from the embeddings where the keys are the words and the values are a vector of embeddings
        """
        try:
            self.words_dict = json.load(open(f'{constants.EMBEDDING_DIR}/words_dict_{self.D}.json'))
        except FileNotFoundError:
            print('no word dictionary found, creating one')
            glove_data_file = f'{constants.EMBEDDING_DIR}/glove.6B.{self.D}d.txt'
            words = pd.read_csv(glove_data_file, sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE)
            self.words_dict = {word: embed for word, embed in zip(words.index, words.values.tolist())}
            with open(f'{constants.EMBEDDING_DIR}/words_dict_{self.D}.json', 'w') as f:
                json.dump(self.words_dict, f)

    def get_embedding_files(self):
        """
        Loads the embedding files
            1. Article embeddings load: contains the average embeddings for all headlines in the cleaned dataset
            2. Image embeddings load: contains the average embeddings for all the image captions in the cleaned dataset
        """
        # embeddings
        try:
            self.image_embeddings_load = np.load(f'{constants.EMBEDDING_DIR}/image_summary_embeddings_{self.D}.npy')
        except FileNotFoundError:
            print(f'no file found, retraining image embeddings with D={self.D}')
            self.train_image_embeddings()
            self.image_embeddings_load = np.load(f'{constants.EMBEDDING_DIR}/image_summary_embeddings_{self.D}.npy')

        try:
            self.article_embeddings_load = np.load(f'{constants.EMBEDDING_DIR}/article_headline_embeddings_{self.D}.npy')
        except FileNotFoundError:
            print(f'no file found, retraining article embeddings with D={self.D}')
            self.train_article_embeddings()
            self.article_embeddings_load = np.load(f'{constants.EMBEDDING_DIR}/article_headline_embeddings_{self.D}.npy')

    def train_article_embeddings(self):
        """
        Trains article embeddings on the headline of the article
        """
        article_embeddings = np.zeros(shape=(len(self.article_summary), self.D))
        for i, text in enumerate(self.article_summary.headline.values):
            text_prep = self.preprocessing(text)
            emb = self.average_embedding(text_prep)
            article_embeddings[i] = self.average_embedding(text_prep)/np.linalg.norm(emb)
        print('saving article embeddings')
        np.save(f'{constants.EMBEDDING_DIR}/article_headline_embeddings_{self.D}.npy', article_embeddings)

    def train_image_embeddings(self):
        """
        Trains image embeddings on the image captions
        """
        image_embeddings = np.zeros(shape=(len(self.image_summary), self.D))
        for i, text in enumerate(self.image_summary.summary.values):
            text_prep = self.preprocessing(text)
            emb = self.average_embedding(text_prep)
            image_embeddings[i] = emb
        print('saving image embeddings')
        np.save(f'{constants.EMBEDDING_DIR}/image_summary_embeddings_{self.D}.npy', image_embeddings)

    def vec(self, w):
        """
        Converts a word to an embedding vector
        """
        try:
            return np.array(self.words_dict[w])
        except:
            return np.zeros(self.D)

    def average_embedding(self, sentence):
        """
        Computes the average embedding of a sentence
        """
        total_embeddings = np.zeros(self.D)
        num_words = len(sentence.split())
        if num_words == 0:
            return total_embeddings
        for word in sentence.split():
            emb = self.vec(word)
            total_embeddings += emb
        avg_embeddings = total_embeddings/num_words
        return avg_embeddings/np.linalg.norm(avg_embeddings)

    def preprocessing(self, sentence):
        """
        Preprocessing. Removes punctuation and stop words
        """
        sentence = sentence.lower().strip()
        bad_chars = '-.?;,!@#$%^&*()+/{}[]\\":\'“’'
        for char in bad_chars:
            sentence = sentence.replace(char, ' ').strip()
        all_words = sentence.split()

        stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again',
                      'there', 'about', 'once', 'during', 'out', 'very', 'having',
                      'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its',
                      'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off',
                      'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the',
                      'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his',
                      'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself',
                      'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both',
                      'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any',
                      'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on',
                      'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why',
                      'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has',
                      'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after',
                      'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
                      'doing', 'it', 'how', 'further', 'was', 'here', 'than']

        filtered_sentence = [w for w in all_words if not w in stop_words]
        return ' '.join(filtered_sentence)

    def predict_articles(self, headline, true_id=None, k=8):
        """
        Predicts the closest matching article headlines given an article headline
        Returns a list of article ids
        """
        text_prep = self.preprocessing(headline)
        emb = self.average_embedding(text_prep)
        emb = emb.reshape(-1,1)/np.linalg.norm(emb)

        # finding nearest neighbors articles
        scores_articles = np.dot(self.article_embeddings_load, emb).flatten()
        if true_id is not None:
            ind = self.article_summary[self.article_summary['headline'] == headline].index.values[0]
            scores_articles[ind] = 0

        top_k_articles = np.argsort(-scores_articles)[:k]
        top_k_art_ids = [self.article_summary.iloc[ind].id for ind in top_k_articles]
        return top_k_art_ids

    def predict_images(self, headline, true_id=None, k=8):
        """
        Predicts the closest matching image caption given an article headline
        Returns a list of image ids
        """
        text_prep = self.preprocessing(headline)
        emb = self.average_embedding(text_prep)
        emb = emb.reshape(-1,1)/np.linalg.norm(emb)

        scores_images = np.dot(self.image_embeddings_load, emb).flatten()
        top_k_images = np.argsort(-scores_images)[:k]
        top_k_img_ids = [self.image_summary.iloc[ind].id for ind in top_k_images]
        return top_k_img_ids
