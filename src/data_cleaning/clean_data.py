#dependencies
import os
import csv
import constants
from remove_item import remove_content_type, remove_foreign_article, remove_article_wo_images
from clean_item import clean_csv

#directory paths
data_directory = constants.DATA_DIR
output_directory = constants.OUTPUT_DIR

#metadata file prefix
article_file_prefix = constants.Text_Prefix
image_file_prefix  = constants.Media_Prefix

#metadata summary files
article_summary_file = f'{data_directory}/{article_file_prefix}summary.csv'
image_summary_file = f'{data_directory}/{image_file_prefix}summary.csv'
new_article_summary_file = f'{output_directory}/{article_file_prefix}summary.csv'
new_image_summary_file = f'{output_directory}/{image_file_prefix}summary.csv'


if __name__ == '__main__':

    ###get list of ids to remove
    #remove audio and video files
    remove_content_type(image_summary_file, ['audio', 'video'], new_image_summary_file)
    #remove non-English articles
    remove_foreign_article(article_summary_file, ['en'], new_article_summary_file)
    #identify articles without images
    remove_article_wo_images(new_image_summary_file, new_article_summary_file)

    print()

    ###clean data
    for filename in os.listdir(data_directory):
        if '.csv' in filename:
            input_file_path = f'{data_directory}/{filename}'
            output_file_path = f'{output_directory}/{filename}'
            #clean csv file
            if article_file_prefix in filename:
                clean_csv(input_file_path, output_file_path, article = True)
            else:
                clean_csv(input_file_path, output_file_path, article = False)
