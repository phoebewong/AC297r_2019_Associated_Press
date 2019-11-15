from src import constants
from format_imp_matrix import get_imp_matrix

#directory path
output_directory = constants.DATA_DIR
#tag types
tags = ['org', 'place', 'subject','person']

if __name__ == '__main__':
    #get image indicator matrix
    get_imp_matrix(output_directory, indicator_matrix = True)
