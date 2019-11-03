import os
import re
import pandas as pd
from src import constants
from collections import defaultdict, Counter

#directory path
train_directory = constants.TRAIN_DIR

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
