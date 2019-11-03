import os
import re
import pandas as pd
from src import constants
from collections import defaultdict, Counter

#directory path
train_directory = constants.TRAIN_DIR

test_file = pd.read_csv(f'{train_directory}/article_summary.csv')

def remove_char(text_string):
    "remove all characters in given text string"
    new_str = re.sub('[\W_]+', ' ', text_string)
    return new_str

def get_sentence(text_string):
    "get sentences from a single input text string"
    svec = re.split(r'[.?!]\s*', text_string)
    #remove space
    while '' in svec:
        svec.remove('')
    return svec

print(get_sentence(test_file.summary.values[0]))

# def format_text(text_string):
#
#
#
# def get_word_dictionaries(train_data_path = train_directory):
#     "get dictionaries for tokenization given training data"

# for i in range(len(test_file.summary.values)):
#     try:
#         print(split_sentences(test_file.summary.values[i])[-1])
#     except:
#         continue
