import json
import numpy as np
import pandas as pd
from src import constants
from scipy.sparse import load_npz, csr_matrix
from sklearn.preprocessing import MinMaxScaler

#directory path
data_directory = constants.DATA_DIR
clean_directory = constants.CLEAN_DIR
#update this in constants.py
imp_matrix_filename = 'imp_matrix.npz'
#load presaved matrix and switch back to dense matrix
img_imp_matrix_sparse = load_npz(f'{data_directory}/{imp_matrix_filename}')
img_imp_matrix = img_imp_matrix_sparse.todense()
#save filename
tag_idx_filename = 'tag_idx.json'
img_idx_filename = 'img_idx.json'
#load index dictionaries
with open(f'{data_directory}/{tag_idx_filename}', 'r') as tag_idx_file, \
     open(f'{data_directory}/{img_idx_filename}', 'r') as img_idx_file:
     tag_idx_dict = json.load(tag_idx_file)
     img_idx_dict = json.load(img_idx_file)

class T2I:
    "class function for tag-to-image recommendation"
    def __init__(self, art_id, ranked_tags, ranked_imp):
        self.idx = art_id #article id
        self.ranked_tags = ranked_tags #tags used in recommendation search
        self.ranked_imp = ranked_imp #tag importance score by textrank
        self.img_imp_matrix_sparse = img_imp_matrix_sparse
        self.img_imp_matrix = img_imp_matrix
        self.tag_vec_shape = self.img_imp_matrix.shape[1]
        self.img_idx_omit = None #record already associated image ids

    def get_associated_images(self):
        "get image ids that have already been associated with article"
        img_summary = pd.read_csv(f'{clean_directory}/{constants.Media_Prefix}summary.csv')
        subset = img_summary[img_summary.article_idx == self.idx]
        self.img_idx_omit = subset.id.values
        print(f'{len(self.img_idx_omit)} associated images found \n')

    def format_tags(self):
        "format ranked tag strings"
        for i in range(len(self.ranked_tags)):
            t = self.ranked_tags[i]
            score = self.ranked_imp[i]
            #replace with formated tags
            self.ranked_tags[i] = t.lower().replace(',', '')

    def prep_article_imp_vec(self):
        "get article importance vector for recommendation"
        #cache article ranked importance vector
        art_imp_vec = np.zeros(self.tag_vec_shape)

        for i in range(len(self.ranked_tags)):
            t = self.ranked_tags[i]
            score = self.ranked_imp[i]
            #find t index
            t_idx = tag_idx_dict[t]
            #update article ranked importance vector
            art_imp_vec[t_idx] = score

        return art_imp_vec

    def predict(self, output_size, method = 'dot_product', remove_original = True):
        "recommend images based on given method"
        #format tags
        self.format_tags()
        if self.img_idx_omit is None:
            #get associated images
            self.get_associated_images()

        #get article ranked importance vector
        art_imp_vec = self.prep_article_imp_vec()

        if method == 'dot_product':
            img_scores = dot_product(self.img_imp_matrix, art_imp_vec)

        # elif method == 'cosine_distance':
        #     #compute dot_product
        #     img_scores = cosine_distance(self.img_imp_matrix_sparse, art_imp_vec)

        #sort for desired number of output
        output_idx = (-img_scores).argsort()

        #get output image ids
        output_img_ids = list()
        for idx in output_idx:
            img_id = list(img_idx_dict.keys())[idx]
            if img_id not in self.img_idx_omit:
                output_img_ids.append(img_id)
                if len(output_img_ids) == output_size:
                    break

        return output_img_ids

def dot_product(ref_matrix, comp_vec):
    '''
    Compute dot product distances between input article
    tag vector and image importance matrix.
    '''
    #normalize matrix and vector
    ref_matrix_normalized = MinMaxScaler().fit_transform(ref_matrix)
    comp_vec_normalized = MinMaxScaler().fit_transform(comp_vec)
    #compute dot_product
    img_scores = np.asarray(np.dot(ref_matrix_normalized, comp_vec_normalized.T)).flatten()
    return img_scores

# def cosine_distance(ref_matrix, comp_vec):
#     '''
#     compute cosine distances between input article
#     tag vector and image importance matrix.
#     '''
#     #reshape vector
#     comp_vec_new = np.repeat(comp_vec.reshape(1,-1), ref_matrix.shape[0], axis = 0)
#     #turn to sparse matrix
#     comp_vec_new = csr_matrix(comp_vec_new)
#     #compute cosine distance
#     img_scores = cosine_similarity(comp_vec_new, ref_matrix)
#     return img_scores[0]
