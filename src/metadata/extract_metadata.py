#dependencies
import os
import csv
import constants
import json
from extract_to_csv import info_to_csv, Summary, AP_Category, Subject, Person, Person_type, \
                           Person_team, Organisation, Org_industry, Place, Event

#directory paths
data_directory = constants.DATA_DIR
output_directory = constants.OUTPUT_CSV_DIR
article_dir_name = constants.ARTICLE_DIR_NAME
image_dir_name = constants.IMAGE_DIR_NAME
search = [article_dir_name, image_dir_name]
if_article = [True, False]

if __name__ == '__main__':
    for dir in search:
        print(f'Writing csv file for {dir}') #track progress
        #get directory path
        full_path = f'{data_directory}/{dir}/'
        #summary csv
        summary_name = 'summary'
        summary_path = f'{output_directory}/{dir}_{summary_name}.csv'
        summary_features = ['id', 'article_idx', 'content_type', 'language',
                            'city', 'country', 'long_lat', 'title', 'headline',
                            'headline_extended', 'summary']
        #output unintended file names
        info_to_csv(summary_name, Summary, summary_path, full_path,
                    summary_features, feature_list = False, article = if_article[search.index(dir)],
                    output_unintended = True)

        #ap category csv
        ap_cat_name = 'ap_category'
        ap_cat_path = f'{output_directory}/{dir}_{ap_cat_name}.csv'
        ap_cat_features = ['id', 'article_idx', 'category_name',
                           'category_relation', 'category_code']
        info_to_csv(ap_cat_name, AP_Category, ap_cat_path, full_path,
                    ap_cat_features, feature_list = True, article = if_article[search.index(dir)])

        #subject tag csv
        subject_name = 'subject'
        subject_path = f'{output_directory}/{dir}_{subject_name}.csv'
        subject_features = ['id', 'article_idx', 'subject_tag',
                            'subject_tag_relation', 'subject_tag_code']
        info_to_csv(subject_name, Subject, subject_path, full_path,
                    subject_features, feature_list = True, article = if_article[search.index(dir)])

        #person tag csv
        person_name = 'person'
        person_path = f'{output_directory}/{dir}_{person_name}.csv'
        person_features = ['id', 'article_idx', 'person_tag',
                           'person_tag_relation', 'person_tag_code']
        info_to_csv(person_name, Person, person_path, full_path,
                    person_features, feature_list = True, article = if_article[search.index(dir)])

        #person type csv
        person_type_name = 'person_type'
        person_type_path = f'{output_directory}/{dir}_{person_type_name}.csv'
        person_type_features = ['id', 'article_idx', 'person_tag',
                                'person_tag_code','person_type']
        info_to_csv(person_type_name, Person_type, person_type_path, full_path,
                    person_type_features, feature_list = True, article = if_article[search.index(dir)])

        #person team csv
        person_team_name = 'person_team'
        person_team_path = f'{output_directory}/{dir}_{person_team_name}.csv'
        person_team_features = ['id', 'article_idx', 'person_tag',
                                'person_tag_code','person_team_tag', 'person_team_code']
        info_to_csv(person_team_name, Person_team, person_team_path, full_path,
                    person_team_features, feature_list = True, article = if_article[search.index(dir)])

        #organisation csv
        org_name = 'org'
        org_path = f'{output_directory}/{dir}_{org_name}.csv'
        org_features = ['id', 'article_idx', 'org_tag',
                        'org_tag_relation', 'org_tag_code']
        info_to_csv(org_name, Organisation, org_path, full_path,
                    org_features, feature_list = True, article = if_article[search.index(dir)])

        #organisation industry csv
        org_industry_name = 'org_industry'
        org_industry_path = f'{output_directory}/{dir}_{org_industry_name}.csv'
        org_industry_features = ['id', 'article_idx', 'org_tag',
                                 'org_tag_code', 'org_industry_tag', 'org_industry_code']
        info_to_csv(org_industry_name, Org_industry, org_industry_path, full_path,
                    org_industry_features, feature_list = True, article = if_article[search.index(dir)])

        #associated place csv
        place_name = 'place'
        place_path = f'{output_directory}/{dir}_{place_name}.csv'
        place_features = ['id', 'article_idx', 'place_tag',
                          'place_tag_relation', 'place_tag_code']
        info_to_csv(place_name, Place, place_path, full_path,
                    place_features, feature_list = True, article = if_article[search.index(dir)])

        #event csv
        event_name = 'event'
        event_path = f'{output_directory}/{dir}_{event_name}.csv'
        event_features = ['id', 'article_idx', 'event_tag', 'place_tag_code']
        info_to_csv(event_name, Event, event_path, full_path,
                    event_features, feature_list = True, article = if_article[search.index(dir)])
