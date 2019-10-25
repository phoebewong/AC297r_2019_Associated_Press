#dependencies
import os
import csv
from src import constants
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
        print(f'Writing csv files for {dir}') #track progress
        #get directory path
        full_path = f'{data_directory}/{dir}/'

        #arguments for data extraction
        funcs = list()
        csv_paths = list()
        feature_lists = list()
        feature_list_args = list()
        article_args = list()

        #summary csv
        funcs.append(Summary)
        summary_path = f'{output_directory}/{dir}_summary.csv'
        csv_paths.append(summary_path)
        summary_features = ['id', 'article_idx', 'version', 'version_created', 'content_type', 'language',
                            'city', 'country', 'long_lat', 'title', 'headline',
                            'headline_extended', 'summary']
        if if_article[search.index(dir)]:
            summary_features.append('full_text')
        feature_lists.append(summary_features)
        feature_list_args.append(False)
        article_args.append(if_article[search.index(dir)])

        #ap category csv
        funcs.append(AP_Category)
        ap_cat_path = f'{output_directory}/{dir}_ap_category.csv'
        csv_paths.append(ap_cat_path)
        ap_cat_features = ['id', 'article_idx', 'category_name',
                           'category_relation', 'category_code']
        feature_lists.append(ap_cat_features)
        feature_list_args.append(True)
        article_args.append(if_article[search.index(dir)])

        #subject tag csv
        funcs.append(Subject)
        subject_path = f'{output_directory}/{dir}_subject.csv'
        csv_paths.append(subject_path)
        subject_features = ['id', 'article_idx', 'subject_tag',
                            'subject_tag_relation', 'subject_tag_code']
        feature_lists.append(subject_features)
        feature_list_args.append(True)
        article_args.append(if_article[search.index(dir)])

        #person tag csv
        funcs.append(Person)
        person_path = f'{output_directory}/{dir}_person.csv'
        csv_paths.append(person_path)
        person_features = ['id', 'article_idx', 'person_tag',
                           'person_tag_relation', 'person_tag_code']
        feature_lists.append(person_features)
        feature_list_args.append(True)
        article_args.append(if_article[search.index(dir)])

        #person type csv
        funcs.append(Person_type)
        person_type_path = f'{output_directory}/{dir}_person_type.csv'
        csv_paths.append(person_type_path)
        person_type_features = ['id', 'article_idx', 'person_tag',
                                'person_tag_code','person_type']
        feature_lists.append(person_type_features)
        feature_list_args.append(True)
        article_args.append(if_article[search.index(dir)])

        #person team csv
        funcs.append(Person_team)
        person_team_path = f'{output_directory}/{dir}_person_team.csv'
        csv_paths.append(person_team_path)
        person_team_features = ['id', 'article_idx', 'person_tag',
                                'person_tag_code','person_team_tag', 'person_team_code']
        feature_lists.append(person_team_features)
        feature_list_args.append(True)
        article_args.append(if_article[search.index(dir)])

        #organisation csv
        funcs.append(Organisation)
        org_path = f'{output_directory}/{dir}_org.csv'
        csv_paths.append(org_path)
        org_features = ['id', 'article_idx', 'org_tag',
                        'org_tag_relation', 'org_tag_code']
        feature_lists.append(org_features)
        feature_list_args.append(True)
        article_args.append(if_article[search.index(dir)])

        #organisation industry csv
        funcs.append(Org_industry)
        org_industry_path = f'{output_directory}/{dir}_org_industry.csv'
        csv_paths.append(org_industry_path)
        org_industry_features = ['id', 'article_idx', 'org_tag',
                                 'org_tag_code', 'org_industry_tag', 'org_industry_code']
        feature_lists.append(org_industry_features)
        feature_list_args.append(True)
        article_args.append(if_article[search.index(dir)])

        #associated place csv
        funcs.append(Place)
        place_path = f'{output_directory}/{dir}_place.csv'
        csv_paths.append(place_path)
        place_features = ['id', 'article_idx', 'place_tag',
                          'place_tag_relation', 'place_tag_code']
        feature_lists.append(place_features)
        feature_list_args.append(True)
        article_args.append(if_article[search.index(dir)])

        #event csv
        funcs.append(Event)
        event_path = f'{output_directory}/{dir}_event.csv'
        csv_paths.append(event_path)
        event_features = ['id', 'article_idx', 'event_tag', 'place_tag_code']
        feature_lists.append(event_features)
        feature_list_args.append(True)
        article_args.append(if_article[search.index(dir)])

        #extract to csv
        info_to_csv(funcs , csv_paths, full_path, feature_lists, feature_list_args, article_args)
