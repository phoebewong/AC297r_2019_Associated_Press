import os
import re
import pandas as pd
import numpy as np
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
    text_string = text_string.replace('\n', ' ')
    svec = re.split(r'[.?!]\s*', text_string)
    #remove space
    while '' in svec:
        svec.remove('')
    return svec

def if_valid(csv_entry):
    "check whether an entry is nan or empty string"
    try:
        np.isnan(csv_entry)
        return False
    except:
        if csv_entry in ['','nan']:
            return False
        else:
            return True
