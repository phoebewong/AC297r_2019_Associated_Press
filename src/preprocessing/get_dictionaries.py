#dependencies
import os
import csv
import pickle
import pandas as pd
import process_utils
from tqdm import tqdm
from src import constants
from collections import defaultdict, Counter

#directory path and output file names
train_directory = constants.TRAIN_DIR
output_directory = constants.DATA_DIR
article_prefix = constants.Text_Prefix
word2idx_filename = constants.word2idx_filename
idx2word_filename = constants.idx2word_filename

#cache dictionaries for tokenization
word2idx = defaultdict(int)
idx2word = defaultdict(str)
wordcnt = Counter()

#add padding and special characters beforehand
word2idx['_'] = 0 #padding characters
word2idx['*'] = 1 #unseen characters, save for test data preprocessing
idx2word[0] = '_'
idx2word[1] = '*'

start_idx = 2

if __name__ == '__main__':
    os.listdir(train_directory)
    for file in os.listdir(train_directory):
        path = f'{train_directory}/{file}'
        # print(path)
        if '.csv' in path:
            print(f'Working on {file}')
            with open(path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for row in tqdm(csv_reader):
                    #if summary file
                    if 'summary' in file:
                        #process full text and captions
                        item = row[-1]
                    #otherwise, process the tags
                    else:
                        if article_prefix in file:
                            item = row[1]
                        else:
                            item = row[2]
                    if item not in ['', 'nan']:
                        #replace special character with space
                        #strip starting and ending white space
                        #split into list
                        item = process_utils.remove_char(item.lower()).strip().split()
                        for i in item:
                            if len(i) > 0:
                                wordcnt[i] += 1
            print()

    print('Processing complete:')
    print(f'Number of tokens: {len(wordcnt)}')
    print('Top 50 Most Common Words:')
    print(wordcnt.most_common(50))
    print()
    print('Making token dictionaries')
    for key in list(wordcnt.keys()):
        word2idx[key] = start_idx
        idx2word[start_idx] = key
        start_idx += 1
    print()
    print('Saving dictionaries to pickle files')
    #save dictionaries to pickle files
    with open(f'{output_directory}/{word2idx_filename}', 'wb') as file_1, \
         open(f'{output_directory}/{idx2word_filename}', 'wb') as file_2:
         pickle.dump(word2idx, file_1)
         pickle.dump(idx2word, file_2)
