import os
import csv
import json
import numpy as np
import pandas as pd
from collections import defaultdict
from scipy.sparse import csc_matrix, save_npz
import sys
from src import constants
sys.path.append(str(constants.PREPROCESSING_DIR))
import process_utils

#directory path
data_directory = constants.CLEAN_DIR
output_directory = constants.DATA_DIR
prefix_list = [constants.Media_Prefix, constants.Text_Prefix]
#tag types
tags = ['org', 'place', 'subject','person']
#presaved tag importance files
obj_imp_filename = constants.obj_imp_filename
scn_imp_filename = constants.scn_imp_filename

#save filename
tag_idx_filename = constants.tag_idx_filename
img_idx_filename = constants.img_idx_filename
imp_matrix_filename = constants.imp_matrix_filename


def get_tag_idx_dictionary(tags, output_directory):
    "initiate a dictionary for tag index"
    i = 0
    track_progress = 0
    tag_idx_dict = defaultdict(int)
    for prefix in prefix_list:
        for tag in tags:
            print(f'Working on {prefix}{tag} file \n')
            file_path = f'{data_directory}/{prefix}{tag}.csv'
            tag_data = pd.read_csv(file_path)
            unique_tags = list(set(tag_data[f'{tag}_tag'].values))
            for t in unique_tags:
                #check validity of tag
                if process_utils.if_valid(t):
                    #format string
                    formatted_tag = t.lower().replace(',', '')
                    if formatted_tag not in list(tag_idx_dict.keys()):
                        tag_idx_dict[formatted_tag] = i
                        i += 1
    print(f'{i} number of tags recorded, saving to {tag_idx_filename} ...')
    with open(f'{output_directory}/{tag_idx_filename}', 'w') as output_file:
        json.dump(tag_idx_dict, output_file)
    print('Complete!')

def get_img_idx_dictionary(output_directory):
    "get a dictionary for image ids"
    i = 0
    track_progress = 0
    img_idx_dict = defaultdict(int)
    obj_imp_file_path = f'{output_directory}/{obj_imp_filename}'
    with open(obj_imp_file_path, 'r') as obj_imp_file:
        obj_imp_dict = json.load(obj_imp_file)
    for key in obj_imp_dict.keys():
        if key not in img_idx_dict.keys():
            img_idx_dict[key] = i
            i += 1
    print(f'{i} image ids recorded, saving to {img_idx_filename} ...')
    with open(f'{output_directory}/{img_idx_filename}', 'w') as output_file:
        json.dump(img_idx_dict, output_file)
    print('Complete!')

def get_imp_matrix(output_directory):
    "get image tag importance matrix from presaved weights files"
    tag_idx_dict_path = f'{output_directory}/{tag_idx_filename}'
    obj_imp_file_path = f'{output_directory}/{obj_imp_filename}'
    scn_imp_file_path = f'{output_directory}/{scn_imp_filename}'
    img_index_file_path = f'{output_directory}/{img_idx_filename}'

    #loading presaved files
    with open(tag_idx_dict_path, 'r') as tag_idx_file, \
         open(img_index_file_path, 'r') as img_idx_file, \
         open(obj_imp_file_path, 'r') as obj_imp_file, \
         open(scn_imp_file_path, 'r') as scn_imp_file:

         tag_idx_dict = json.load(tag_idx_file)
         img_idx_dict = json.load(img_idx_file)
         obj_imp_dict = json.load(obj_imp_file)
         scn_imp_dict = json.load(scn_imp_file)

    #height of matrix
    length = len(img_idx_dict)
    #width of matrix
    width = len(tag_idx_dict)

    print(f'Image importance matrix shape: {length} x {width}')

    #initiate matrix
    imp_matrix = np.zeros((length, width))

    labels = ['object tags', 'scene tags']
    checklist = [obj_imp_dict, scn_imp_dict]
    for i in range(len(labels)):
        print(f'Working on {labels[i]} \n')
        for img_id in checklist[i].keys():
            #get image id index from dictionary
            matrix_idx = img_idx_dict[img_id]
            for t, val in checklist[i][img_id].items():
                #get tag index
                t_idx = tag_idx_dict[t]
                #replace value in matrix
                imp_matrix[matrix_idx, t_idx] = val

    #save as sparse matrix
    print(f'Saving to {imp_matrix_filename} ...')
    sparse_matrix = csc_matrix(imp_matrix)
    save_npz(f'{output_directory}/{imp_matrix_filename}', sparse_matrix)
    print('Complete!')
