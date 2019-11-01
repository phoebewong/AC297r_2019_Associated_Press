import os
import numpy as np
from src import constants

#duplicate image id files
dup_img_file = constants.IMAGE_DUPLICATES_FILENAME

def modify_duplicates(img_id):
    "check whether image is a duplicate"
    with open(dup_img_file, 'r') as dup_idx:
        for line in dup_idx.readlines():
            list_id = line.rstrip().split(',')
            #reference id
            id_ref = list_id[0]
            #if image is a duplicate, return reference id
            if img_id in list_id:
                return id_ref
    #otherwise, return img_id
    return img_id
