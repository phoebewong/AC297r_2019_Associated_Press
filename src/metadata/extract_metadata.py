#dependencies
import os
import csv
import constants
import json
from process_metadata import Metadata

#directory paths
data_directory = constants.DATA_DIR
article_dir_name = constants.ARTICLE_DIR_NAME
image_dir_name = constants.IMAGE_DIR_NAME
data_truth = constants.DATA_TRUTH

search = [article_dir_name, image_dir_name]
data_truth_path = f'{data_directory}/{data_truth}'

if __name__ == '__main__':
    for dir in search:
        #get directory path
        #create csv file
        full_path = f'{data_directory}/{dir}/'
        csv_file_intended_path = f'{data_directory}/{dir}_metadata.csv'
        csv_file_unintended_path = f'{data_directory}/{dir}_metadata_unintended.csv'
        print(f'Writing csv file for {dir}') #track progress
        #feature names
        features = ['id', 'article_id', 'content_type', 'language',
                    'city', 'country', 'title', 'headline',
                    'headline_extended', 'summary', 'keyword',
                    'tag', 'tag_relation']
        #id = article_id for articles
        if dir == article_dir_name:
            features.remove('article_id')

        #verify if data is intended for project
        #save to separate csv files
        with open(csv_file_intended_path, 'w') as content_intended_csv, open(csv_file_unintended_path, 'w') as content_unintended_csv:
            csv_writer_intended = csv.writer(content_intended_csv)
            csv_writer_unintended = csv.writer(content_unintended_csv)
            csv_writer_intended.writerow(features)
            csv_writer_unintended.writerow(features)
            for file in os.listdir(full_path):
                #check if json file
                if '.json' in file:
                    #load file
                    file_path = f'{full_path}/{file}'
                    content_json = json.load(open(file_path, "rb" ))

                    #initiate metadata extraction
                    content = Metadata(content_json)

                    #get content Metadata
                    #for now get content for eda
                    idx = content.id
                    article_idx = content.ai
                    content_type = content.type
                    language = content.language

                    #content location info
                    city = content.get_city()
                    country = content.get_country_name()

                    #content description info
                    title = content.get_title()
                    headline = content.get_headline()
                    headline_extended = content.get_headline_extended()
                    summary = content.get_summary()
                    keywords = content.get_keywords() #returns a list
                    tags, tag_relations = content.get_subjects() #returns lists

                    if content_type == 'text':
                        feature_vals = [idx, content_type, language,
                                        city, country, title, headline,
                                        headline_extended, summary]
                    else:
                        feature_vals = [idx, article_idx, content_type, language,
                                        city, country, title, headline,
                                        headline_extended, summary]
                    #create an entry for each combination
                    for k in keywords:
                        for i in range(len(tags)):
                            feature_vals_comb = feature_vals + [k, tags[i], tag_relations[i]]

                            with open(data_truth_path, 'r') as file_truth:
                                if (str(idx) in file_truth.read()) or (str(article_idx) in file_truth.read()):
                                    #write value to csv
                                    csv_writer_intended.writerow(feature_vals_comb)
                                else:
                                    csv_writer_unintended.writerow(feature_vals_comb)

                                file_truth.close()
