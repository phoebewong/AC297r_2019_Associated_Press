from src import constants
import numpy as np
import pandas as pd
import csv
import json
import pickle
# NLP
from gensim.corpora import Dictionary
from gensim.models import Word2Vec, WordEmbeddingSimilarityIndex
from gensim.similarities import SoftCosineSimilarity, SparseTermSimilarityMatrix

class SoftCosine:
    "class function for tag-to-image recommendation"
    def __init__(self, num_best=10):
        # dimension of embeddings to use
        # self.D = D

        # get words dictionary
        # self.get_words_dict()

        # data
        self.article_summary = pd.read_csv(f'{constants.CLEAN_DIR}/{constants.Text_Prefix}summary.csv')
        self.image_summary =  pd.read_csv(f'{constants.CLEAN_DIR}/{constants.Media_Prefix}summary.csv')

        # get embeddings
        self.get_embedding_files(num_best=num_best)

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

    def get_embedding_files(self, num_best = 10):
        """
        Get the dictionary, bow_corpos, similiarity matrix and docsim index pre-trained on all image tags.
        """
        # embeddings
        try:
            with open(f'{constants.EMBEDDING_DIR}/soft_cosine.pkl', "rb") as f:
                self.dictionary, self.bow_corpus, self.similarity_matrix, _ = pickle.load(f)
            self.docsim_index = SoftCosineSimilarity(self.bow_corpus, self.similarity_matrix, num_best=num_best)

        except FileNotFoundError:
            print(f'no file found, training word2vec to get bow_corpus, similarity matrix and docsim index')
            # read in all tags
            try:
                with open(f'{constants.DATA_DIR}/all_img_tags.pkl', 'rb') as fp:
                    all_img_tags_lower = pickle.load(fp)
            except FileNotFoundError:
                print(f'no file found at {constants.DATA_DIR}/all_img_tags.pkl')
            model = Word2Vec(all_img_tags_lower, size=20, min_count=1)  # train word2vec
            termsim_index = WordEmbeddingSimilarityIndex(model.wv)
            self.dictionary = Dictionary(all_img_tags_lower)
            self.bow_corpus = [self.dictionary.doc2bow(document) for document in all_img_tags_lower]
            self.similarity_matrix = SparseTermSimilarityMatrix(termsim_index, self.dictionary)  # construct similarity matrix
            # 10 (default) most similar image tag vectors
            self.docsim_index = SoftCosineSimilarity(self.bow_corpus, self.similarity_matrix, num_best=num_best)
            print(f'Saving bow_corpus, similarity matrix and docsim index to {constants.EMBEDDING_DIR}')
            with open(f'{constants.EMBEDDING_DIR}/soft_cosine.pkl', "wb") as f:
                pickle.dump((self.dictionary, self.bow_corpus, self.similarity_matrix, self.docsim_index), f)

    def if_valid(self, csv_entry):
        "check whether an entry is nan or empty string"
        try:
            np.isnan(csv_entry)
            return False
        except:
            if csv_entry in ['', 'nan']:
                return False
            else:
                return True

    def get_tags(self, idx, prefix, tag_types):
        """Helper function to get tags"""
        "get list of tags"
        # Reading in directory names
        clean_dir = constants.CLEAN_DIR
        art_prefix = constants.Text_Prefix
        img_prefix = constants.Media_Prefix
        # Get tags
        at = list()
        for tt in tag_types:
            data = pd.read_csv(f'{clean_dir}/{prefix}{tt}.csv')
            subset = data[data.id == idx]
            tag_list = subset[f'{tt}_tag'].values
            for t in tag_list:
                # check validity of tag
                if self.if_valid(t):
                    at.append(t)
        return at

    # def vec(self, w):
    # def get_article_id(self, title):
    #     """
    #     Get the ID of the input article ID
    #     Can be removed once tagging API integration is done.
    #     """
    #     try:
    #         art_id = self.article_summary[self.article_summary['title'] == title].id
    #         return art_id
    #     except:
    #         print("Article not found in the data, therefore, cannot find its article ID")

    def predict(self, title, art_id = None, num_best = 10, tag_types = ['org', 'place', 'subject', 'person']):
        """
        Predicts the closest 10 matching image tag vectors given an article tag vector
        Returns a list of image ids
        """
        try:
            with open(f'{constants.DATA_DIR}/scene_tag_importance_all.json') as json_file:
                scene_tag_importance = json.load(json_file)
            all_img_id = np.array(list(scene_tag_importance.keys()))
        except FileNotFoundError:
            print(f'no file found at {constants.DATA_DIR}/scene_tag_importance_all.json')
        # Get article ID
        # art_id = self.get_article_id(title)
        # Get article tags and lowercase them
        art_tags_lower = list(map(lambda x: x.lower(), self.get_tags(art_id, 'article_', tag_types)))
        # Compare target article tags with other image tags
        # calculate top 10 similar of tags to pre-trained word2vec document similiary index on all images
        sims = self.docsim_index[self.dictionary.doc2bow(art_tags_lower)] # [(ix1, score1), (ix2, score2),....]
        # Get top 10 similar image ID
        top_10_img_id = [all_img_id[sim[0]] for sim in sims]
        return top_10_img_id
