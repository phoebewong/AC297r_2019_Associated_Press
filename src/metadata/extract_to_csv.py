import os
import csv
import json
from process_metadata import Metadata
from verify_data import intended_data

def info_to_csv(info_type, func, csv_path, data_path, features, \
                feature_list = False, article = False, output_unintended = False):
    '''
    write csv for an input metadata field

    Params:
    -------
    1) info_type: string, metadata field to extract, for the purpose of tracking progress
    2) func: function, function to extract metadata fields, see functions below
    3) csv_path: string, output csv file path
    4) data_path: string, data directory path
    5) features: list or array-like, csv headers
    6) feature_list: boolean, whether output metadatafield would be a list
    7) article: boolean, whether processed content type is text
    8) output_unintended: boolean, if true, outputs unindended file ids

    Return:
    -------
    metadata csv files in output directory
    '''
    if article:
        #remove article idx from text files as this field would be None
        features.remove('article_idx')
    with open(csv_path, 'w') as file_csv:
        file_writer = csv.writer(file_csv)
        #write headers
        file_writer.writerow(features)
        cnt = 0 #track progress
        unintended = 0 #track unintended data file
        for file in os.listdir(data_path):
            #track progress
            cnt += 1
            if cnt % 1000 == 0:
                print(f'Working on file # {cnt} {info_type}')
            #check if json file
            if '.json' in file:

                #load json file
                file_path = f'{data_path}/{file}'
                content_json = json.load(open(file_path, "rb" ))

                #initiate metadata extraction
                content = Metadata(content_json)
                idx = content.id
                article_idx = content.ai

                #check if data is intended for use
                if intended_data(idx, article_idx):
                    content_type = content.type
                    feature_vals = [idx, article_idx]
                    if content_type == 'text':
                        #article idx is None for text files
                        feature_vals.remove(article_idx)
                    #get metadata
                    info_vals = func(content)
                    if info_vals is not None:
                        #if output metadata is a list
                        #loop through outputs and get
                        #combinations of all entries
                        if feature_list:
                            for i in range(len(info_vals[0])):
                                file_writer.writerow(feature_vals + [val[i] for val in info_vals])
                        else:
                            file_writer.writerow(feature_vals + info_vals)
                else:
                    unintended += 1 #track unintended files
                    #output unintended file names if asked
                    if output_unintended:
                        print(f'{idx} not for project')
                        if article_idx is None:
                            print(f'{idx} not for project')
                        else:
                            print(f'{article_idx} not for project')
    #track progress
    print(f'{csv_path} complete')
    print(f'{unintended} files found')
    print()

def Summary(content):
    "extract article descriptive data"
    content_type = content.type
    language = content.language
    city = content.get_city()
    country = content.get_country_name()
    long_lat = content.get_long_lat()
    version = content.version
    version_created = content.versioncreated

    #content description info
    title = content.get_title()
    headline = content.get_headline()
    headline_extended = content.get_headline_extended()
    summary = content.get_summary()

    feature_vals = [version, version_created, content_type, language,
                    city, country, long_lat, title, headline,
                    headline_extended, summary]
    return feature_vals

def AP_Category(content):
    "extract AP category code"
    feature_vals = content.get_AP_category()
    return feature_vals

def Subject(content):
    "extract subject tags"
    feature_vals = content.get_subjects()
    return feature_vals

def Person(content):
    "extract person tags"
    feature_vals = content.get_person_tags()
    return feature_vals

def Person_type(content):
    "extract person type tags"
    feature_vals = content.get_person_types()
    return feature_vals

def Person_team(content):
    "extract person team tags"
    feature_vals = content.get_person_team()
    return feature_vals

def Organisation(content):
    "extract organisation tags"
    feature_vals = content.get_organisation()
    return feature_vals

def Org_industry(content):
    "extract organisation industry tags"
    feature_vals = content.get_organisation_industry()
    return feature_vals

def Place(content):
    "extract content assocaited place tags"
    feature_vals = content.get_place()
    return feature_vals

def Event(content):
    "extract event tags"
    feature_vals = content.get_event_tags()
    return feature_vals
