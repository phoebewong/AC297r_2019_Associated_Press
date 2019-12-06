#import packages
import json
import numpy as np
import pandas as pd
from src import constants
import sys
sys.path.append('../')
from scipy.sparse import load_npz
from sklearn.preprocessing import Normalizer
import tensorflow as tf
import tensorflow_hub as hub

class USE_Recsys:
    "text-to-text image recommendation with USE"
    def __init__(self):
        self.load_models_and_files()

    def load_models_and_files(self):
        "loads the models and files"

        #load presaved files
        article_summary_path = f'{constants.CLEAN_DIR}/{constants.Text_Prefix}summary.csv'
        image_summary_path = f'{constants.CLEAN_DIR}/{constants.Media_Prefix}summary.csv'

        #read as df
        df_article = pd.read_csv(article_summary_path)
        df_image = pd.read_csv(image_summary_path)
        data_directory = constants.DATA_DIR

        #load presaved matrix and switch back to dense matrix
        print(f'Loading image place tag indicator matrix...')
        img_place_ind_matrix_sparse = load_npz(f'{data_directory}/image_place_tag_ind_matrix.npz')
        self.img_place_ind_matrix = img_place_ind_matrix_sparse.todense()
        print('Loading place tags...')
        self.place_tags = list()

        with open(f'{data_directory}/place_tag_list.txt', 'r') as place_tag_list:
            for line in place_tag_list:
                pt = line[:-1]
                self.place_tags.append(pt)

        #load presaved img bert embeddings
        print(f'Loading presaved image USE embeddings...')
        img_USE_embedding = np.load(f'{constants.DATA_DIR}/{constants.img_USE_embedding_matrix_filename}')['arr_0']

        #normalizing matrix
        print(f'Normalizing matrix...')
        self.img_USE_embedding = Normalizer().fit_transform(img_USE_embedding)

        #save filename
        img_idx_filename = constants.img_idx_filename

        #load index dictionaries
        with open(f'{constants.DATA_DIR}/{img_idx_filename}', 'r') as img_idx_file:
            self.img_idx_dict = json.load(img_idx_file)

        #load pretrained sentence embeddings
        print(f'Loading pretrained USE...')
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


    def get_article_embedding(self, article_headline):
        "get article headline embedding"
        #normalize embedding
        return self.embed([article_headline])

    # def get_associated_images(self, article_id):
    #     "get image ids that have already been associated with article"
    #     if article_id is None:
    #         print('Input article id for operation')
    #     else:
    #         img_summary = pd.read_csv(f'{constants.CLEAN_DIR}/{constants.Media_Prefix}summary.csv')
    #         subset = img_summary[img_summary.article_idx == article_id]
    #         return subset.id.values

    def remove_images(self, article_tags):
        "remove image candidates based on place tag overlaps"
        #get article place tag indicator matrix
        article_place_tag_idx = list()
        for pt in self.place_tags:
            if pt in article_tags:
                article_place_tag_idx.append(1)
            else:
                article_place_tag_idx.append(0)
        if 1 not in article_place_tag_idx:
            self.remove_image_idx = None
        else:
            check_overlap = np.asarray(np.dot(self.img_place_ind_matrix, np.array(article_place_tag_idx).T)).flatten()
            self.remove_image_idx = np.where(check_overlap == 0)[0]

    def predict(self, article_headline, article_tags = None, article_id = None, output_size=16):
        "recommend images by cosine similarity"
        article_embedding = self.get_article_embedding(article_headline)
        article_tags = [t.lower().replace(',', '') for t in article_tags] # article tags in dataset or by tagging api
        self.remove_images(article_tags)
        #get image cosine similarity scores
        img_scores = dot_product(self.img_USE_embedding, article_embedding)
        #sort for desired number of output
        output_idx = (-img_scores).argsort()
        #get output image ids
        output_img_ids = list()
        for idx in output_idx:
            img_id = list(self.img_idx_dict.keys())[idx]
            if self.remove_image_idx is None:
                output_img_ids.append(img_id)
            elif idx not in self.remove_image_idx:
                output_img_ids.append(img_id)
            if len(output_img_ids) == output_size:
                break
        return output_img_ids

def dot_product(ref_matrix, comp_vec):
    '''
    Compute dot product distances between input article
    tag vector and image importance matrix.
    '''
    # #normalize vector
    comp_vec_normalized = Normalizer().fit_transform(comp_vec).flatten()
    #compute dot_product
    img_scores = np.asarray(np.dot(ref_matrix, comp_vec_normalized.T)).flatten()
    return img_scores

###demo###
# def if_valid(csv_entry):
#     "check whether an entry is nan or empty string"
#     try:
#         np.isnan(csv_entry)
#         return False
#     except:
#         if csv_entry in ['','nan']:
#             return False
#         else:
#             return True
#
# def get_place_tags(idx):
#     "get list of tags"
#     pt = list()
#     data = pd.read_csv(f'{constants.CLEAN_DIR}/{constants.Text_Prefix}place.csv')
#     subset = data[data.id == idx]
#     tag_list = subset.place_tag.values
#     for t in tag_list:
#         #check validity of tag
#         if if_valid(t):
#             pt.append(t)
#     return pt

# def get_headline(idx, data = df_image):
#     "get image caption"
#     subset = data[data.id == idx]
#     return subset.headline.values
#
# def output_headline(label, id_list):
#     print(f'{label}: \n')
#     for idx in id_list:
#         print(get_headline(idx))
#
# def prediction_demo(test_article_headline, test_article_tags, test_article_id, recommend_size):
#     print(f'Test Article Headline: {test_article_headline} \n')
#     USE_recsys_object = USE_Recsys(test_article_headline, test_article_tags, test_article_id)
#     print(f'Searching for associated images ...\n')
#     associated_img = USE_recsys_object.get_associated_images()
#     print(f'Recommending {recommend_size} images ...\n')
#     predicted_img_idx = USE_recsys_object.predict(output_size = recommend_size)
#     output_headline('Recommended Images', predicted_img_idx)
#     print()
#     output_headline('True Images', associated_img)

# if __name__ == '__main__':
#     # #preview dir
#     # preview_dir = f'{constants.DATA_DIR}/preview'
#     #get random article
#     exp_id = np.random.choice(df_article.id.values)
#     exp_headline = df_article[df_article.id == exp_id].headline.values[0]
#     exp_place_tags = get_place_tags(exp_id)
#     prediction_demo(exp_headline, exp_place_tags, exp_id, 8)
