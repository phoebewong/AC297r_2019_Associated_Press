import os
import csv
import json
from process_metadata import Metadata
from verify_data import intended_data


def info_to_csv(funcs, csv_paths, data_path, feature_lists, \
                feature_list_args, article_args):
    '''
    Params:
    -------
    1) funcs: functions, functions to extract metadata fields,
       see functions below
    2) csv_paths: list or array-like, output csv file paths
    3) data_path: string, data directory path
    4) feature_lists: list or array-like, csv headers
    5) feature_list_args: list or array-like, list of boolean arguments
       indicating whether output metadatafield would be a list
    6) article_args: list or array-like, list of boolean arguments
       indicating whether processed content type is text

    Return:
    -------
    metadata csv files in output directory
    '''

    #track number of files extracted
    cnt = 0
    #track unintended file
    unintended = list()

    #writer csv headers
    for i in range(len(csv_paths)):
        headers = feature_lists[i]
        if article_args[i]:
            #remove article idx from text files as this field would be None
            headers.remove('article_idx')
        with open(csv_paths[i], 'w', newline='', encoding='utf-8') as file_csv:
            file_writer = csv.writer(file_csv)
            #write headers
            file_writer.writerow(headers)

    #go through each data file in directory
    for file in os.listdir(data_path):
        #track progress
        cnt += 1
        if cnt % 1000 == 0:
            print(f'Working on file # {cnt}')
        #check if json file
        if '.json' in file:
            #load json file
            file_path = f'{data_path}/{file}'
            content_json = json.load(open(file_path, "rb" ))
            #initiate metadata extraction
            content = Metadata(content_json)
            idx = content.id
            article_idx = content.ai
            #extract if data is intended for use
            if intended_data(idx, article_idx):
                #track number of metadata extracted
                i = 0
                #extract all requested info types
                while i < len(funcs):
                    with open(csv_paths[i], 'a') as file_csv:
                        file_writer = csv.writer(file_csv)
                        content_type = content.type
                        feature_vals = [idx, article_idx]

                        if content_type == 'text':
                            #article idx is None for text files
                            feature_vals.remove(article_idx)

                        #get metadata
                        info_vals = funcs[i](content)

                        if info_vals is not None:
                            #if output metadata is a list
                            #loop through outputs and get
                            #combinations of all entries
                            if feature_list_args[i]:
                                for m in range(len(info_vals[0])):
                                    file_writer.writerow(feature_vals + [val[m] for val in info_vals])
                            else:
                                file_writer.writerow(feature_vals + info_vals)
                        i += 1
            else:
                if idx not in unintended:
                    unintended.append(idx) #track unintended files

    #report end progress
    print()
    if len(unintended) > 0:
        print(f'{len(unintended)} unintended files:')
        for f in unintended:
            print(f)
    else:
        print('0 unintended files identified, extraction complete')
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
    #extract full text if article
    if content_type == 'text':
        full_text = content.get_full_text()
        feature_vals.append(full_text)
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
