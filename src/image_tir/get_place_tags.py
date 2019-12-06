###run to extract place tags for articles and images
import json
import time
import numpy as np
import pandas as pd
from src import constants
from scipy.sparse import load_npz, csc_matrix, save_npz

data_directory = constants.DATA_DIR
clean_directory = constants.CLEAN_DIR
article_place = pd.read_csv(f'{clean_directory}/{constants.Text_Prefix}place.csv')
image_place = pd.read_csv(f'{clean_directory}/{constants.Media_Prefix}place.csv')

#save filename
img_idx_filename = constants.img_idx_filename
tag_idx_filename = constants.tag_idx_filename
#load index dictionaries
with open(f'{constants.DATA_DIR}/{img_idx_filename}', 'r') as img_idx_file, \
     open(f'{constants.DATA_DIR}/{tag_idx_filename}', 'r') as tag_idx_file, \
     open(f'{data_directory}/place_tag_idx.json', 'r') as place_tag_idx_file:
     img_idx_dict = json.load(img_idx_file)
     tag_idx_dict = json.load(tag_idx_file)

#get all place tags from directory
i = 0
place_tag = list()
place_tag_idx = list()
search = [article_place.place_tag.values, image_place.place_tag.values]
for vec in search:
    for p_tag in vec:
        try:
            format_p_tag = p_tag.lower().replace(',', '')
            p_idx = tag_idx_dict[format_p_tag]
            #get tag index
            if p_idx not in place_tag_idx:
                place_tag_idx.append(p_idx)
                place_tag.append(format_p_tag)
        except:
            continue

#update this in constants.py
ind_matrix_filename = constants.ind_matrix_filename
#load presaved matrix and switch back to dense matrix
ind_matrix_sparse = load_npz(f'{data_directory}/{ind_matrix_filename}')
img_ind_matrix = ind_matrix_sparse.todense()

#slice matrix
img_place_ind_matrix = img_ind_matrix[:, place_tag_idx]
print(f'Saving to place tag indicator matrix ...')
save_npz(f'{data_directory}/image_place_tag_ind_matrix.npz', csc_matrix(img_place_ind_matrix))
print(f'Saving place tag list')
with open(f'{data_directory}/place_tag_list.txt', 'w') as outputfile:
    for pt in place_tag:
        outputfile.write(f'{pt}\n')
