from src import constants
from format_imp_matrix import get_tag_idx_dictionary, get_imp_matrix, get_img_idx_dictionary

#directory path
output_directory = constants.DATA_DIR
#tag types
tags = ['org', 'place', 'subject','person']

if __name__ == '__main__':
    #get tag index dictionary
    get_tag_idx_dictionary(tags, output_directory)
    #get image index dictionary
    get_img_idx_dictionary(output_directory)
    #get image importance matrix
    get_imp_matrix(output_directory)
