import csv
from src import constants
from create_duplicates import modify_duplicates

#cleaning history output
history_dir = constants.HIST_DIR
hist_content_type_name = constants.media_removal_hist_name
hist_article_name = constants.article_removal_hist_name

#txt files recording ids for removal
img_removal_file = f'{history_dir}/{hist_content_type_name}'
article_removal_file = f'{history_dir}/{hist_article_name}'

def check_removal(id, remove_id_file):
    "check whether id is in to-remove list"
    with open(remove_id_file, 'r') as remove:
        if id in remove.read():
            remove.close()
            return True
        else:
            remove.close()
            return False

def clean_csv(old_file, new_file, article = True):
    "remove unwanted ids from original csv files"
    #track progress
    filename = old_file.split('/')[-1]
    print(f'Cleaning {filename}')
    num_obs_old = 0
    num_obs_new = 0
    with open(old_file, 'r') as input_file, \
         open(new_file, 'w') as output_file:

         csv_reader = csv.reader(input_file)
         csv_writer = csv.writer(output_file)

         #get header of csv file
         header = next(csv_reader)
         csv_writer.writerow(header)
         if article:
             #find article id, content type index
             idx_id = header.index('id')
             for row in csv_reader:
                 num_obs_old += 1
                 if check_removal(row[idx_id], article_removal_file) == False:
                     num_obs_new += 1
                     csv_writer.writerow(row)
         else:
             #find img, article ids
             idx_iid, idx_aid =  header.index('id'), header.index('article_idx')
             for row in csv_reader:
                 num_obs_old += 1
                 if (check_removal(row[idx_iid], img_removal_file) == False) and (check_removal(row[idx_aid], article_removal_file) == False):
                     num_obs_new += 1
                     #check if image is a duplicate and replace id
                     row[idx_iid] = modify_duplicates(row[idx_iid])
                     csv_writer.writerow(row)
    print(f'pre-cleaning # observations: {num_obs_old}')
    print(f'post-cleaning # observations: {num_obs_new}')
    print()
