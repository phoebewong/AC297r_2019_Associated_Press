import json
import numpy as np
import pandas as pd
from src import constants
from scipy.sparse import load_npz

#directory path
data_directory = constants.DATA_DIR
clean_directory = constants.CLEAN_DIR
#update this in constants.py
imp_matrix_filename = 'imp_matrix.npz'
#save filename
tag_idx_filename = 'tag_idx.json'
img_idx_filename = 'img_idx.json'
#load presaved matrix and switch back to dense matrix
img_imp_matrix = load_npz(f'{data_directory}/{imp_matrix_filename}').todense()

class T2I:
    "class function for tag-to-image recommendation"
    def __init__(self, art_id, ranked_tags, ranked_imp):
        self.idx = art_id #article id
        self.ranked_tags = ranked_tags #tags used in recommendation search
        self.ranked_imp = ranked_imp #tag importance score by textrank
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

    def predict(self, output_size, method = 'dot_product', remove_original = True):
        "recommend images based on given method"
        #load index dictionaries
        with open(f'{data_directory}/{tag_idx_filename}', 'r') as tag_idx_file, \
             open(f'{data_directory}/{img_idx_filename}', 'r') as img_idx_file:
             tag_idx_dict = json.load(tag_idx_file)
             img_idx_dict = json.load(img_idx_file)

        #format tags
        self.format_tags()
        if self.img_idx_omit is None:
            #get associated images
            self.get_associated_images()

        #cache article ranked importance vector
        art_imp_vec = np.zeros(self.tag_vec_shape)

        for i in range(len(self.ranked_tags)):
            t = self.ranked_tags[i]
            score = self.ranked_imp[i]
            #find t index
            t_idx = tag_idx_dict[t]
            #update article ranked importance vector
            art_imp_vec[t_idx] = score

        if method == 'dot_product':
            #compute dot_product
            img_scores = np.asarray(np.dot(self.img_imp_matrix, art_imp_vec.T))
            flatten_img_scores = img_scores.flatten()
            #sort for desired number of output
            output_idx = (-flatten_img_scores).argsort()

        #get output image ids
        output_img_ids = list()
        for idx in output_idx:
            img_id = list(img_idx_dict.keys())[idx]
            if img_id not in self.img_idx_omit:
                output_img_ids.append(img_id)
                if len(output_img_ids) == output_size:
                    break

        return output_img_ids
