#package dependencies
import os
import csv
import numpy as np
import pandas as pd
from src import constants
from sklearn.model_selection import train_test_split

#get directory path and constant variables
data_directory = constants.CLEAN_DIR
output_directory = constants.TRAIN_TEST_DIR
output_train_dir = constants.TRAIN_DIR
output_test_dir = constants.TEST_DIR
output_val_dir = constants.VAL_DIR
output_train_txt = constants.train_aid_filename
output_test_txt = constants.test_aid_filename
output_val_txt = constants.val_aid_filename
random_state = constants.data_split_random_state
article_prefix = constants.Text_Prefix
image_prefix = constants.Media_Prefix
test_size = constants.test_size
val_size = constants.val_size


if __name__ == '__main__':

    #read in article summary data
    article_summary_file = f'{data_directory}/{article_prefix}summary.csv'
    article_data = pd.read_csv(article_summary_file)
    article_ids = article_data.id.values
    #train-test split
    train, test = train_test_split(article_ids, test_size = test_size+val_size, random_state = random_state)
    #test-validation split
    test, val = train_test_split(article_ids, test_size = val_size, random_state = random_state)

    #save to txt
    print(f'{len(train)} training article ids')
    print(f'Writing {output_train_txt}')
    np.savetxt(f'{output_directory}/{output_train_txt}', train, fmt='%s')
    print()
    print(f'{len(test)} test article ids')
    print(f'Writing {output_test_txt}')
    np.savetxt(f'{output_directory}/{output_test_txt}', test, fmt='%s')
    print()
    print(f'{len(val)} validation article ids')
    print(f'Writing {output_val_txt}')
    np.savetxt(f'{output_directory}/{output_val_txt}', val, fmt='%s')
    print()

    #get train, test, and validation data
    for file in os.listdir(data_directory):
        if '.csv' in file:
            print(f'Train-Val-Test Split on {file}')
            #track progress
            total_cnt = 0
            train_cnt = 0
            test_cnt = 0
            val_cnt = 0
            #file paths
            file_path = f'{data_directory}/{file}'
            train_path = f'{output_train_dir}/{file}'
            test_path = f'{output_test_dir}/{file}'
            val_path = f'{output_val_dir}/{file}'
            #train test split
            with open(file_path, 'r') as original_file, \
                 open(train_path, 'w+') as train_file, \
                 open(test_path, 'w+') as test_file, \
                 open(val_path, 'w+') as val_file:
                 read_file = csv.reader(original_file)
                 #get header of csv file
                 header = next(read_file)
                 write_train = csv.writer(train_file)
                 write_test = csv.writer(test_file)
                 write_val = csv.writer(val_file)
                 #write header
                 write_train.writerow(header)
                 write_test.writerow(header)
                 write_val.writerow(header)
                 if article_prefix in file:
                     #find article id
                     idx_id = header.index('id')
                 else:
                     #find article id
                     idx_id = header.index('article_idx')
                 for row in read_file:
                     total_cnt += 1
                     if row[idx_id] in train:
                         train_cnt += 1
                         write_train.writerow(row)
                     elif row[idx_id] in test:
                         test_cnt += 1
                         write_test.writerow(row)
                     elif row[idx_id] in val:
                         val_cnt += 1
                         write_val.writerow(row)

            print(f'Original Set: {total_cnt} observations')
            print(f'Training Set: {train_cnt} observations')
            print(f'Validation Set: {val_cnt} observations')
            print(f'Test Set: {test_cnt} observations')
            print()
