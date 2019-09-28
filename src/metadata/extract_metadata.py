

#dependencies
import os
import csv
import json
from process_metadata import Metadata

#directory paths
data_directory = '../../data'
article_directory = 'article'
image_directory = 'image'

search = [article_directory, image_directory]

if __name__ == '__main__':
    for dir in search:
        #get directory path
        #create csv file
        full_path = f'{data_directory}/{dir}/'
        csv_file_path = f'{data_directory}/{dir}_metadata.csv'
        with open(csv_file_path, 'w') as content_csv:
            csv_writer = csv.writer(content_csv)
            #feature names
            features = ['id', 'content_type', 'language',
                        'city', 'country', 'title', 'headline',
                        'headline_extended', 'summary', 'keyword',
                        'tag', 'tag_relation']
            csv_writer.writerow(features)
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

                    feature_vals = [idx, content_type, language,
                                    city, country, title, headline,
                                    headline_extended, summary]

                    #create an entry for each combination
                    for k in keywords:
                        for i in range(len(tags)):
                            feature_vals_comb = feature_vals + [k, tags[i], tag_relations[i]]
                            #write value to csv
                            csv_writer.writerow(feature_vals_comb)
