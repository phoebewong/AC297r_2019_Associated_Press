###extarct taxonomy subset
###api executes tree search on taxonomy dataset

import json
import requests
import constants
import configparser

output_dir = constants.OUTPUT_CSV_DIR

#retrieve password
config = configparser.ConfigParser()
config.read('password.ini')
taxonomy_apikey =  (config['key']['apikey'])

def get_taxonomy_subset(dataset, GUID, format = 'json'):
    '''
    get taxonomy subset

    Params:
    -------
    1) dataset: string, name of taxonomy dataset to search
    2) GUID: string, id of taxonomy term to search
    3) format: string, return request format
    '''

    request_url = f'http://cv.ap.org/d/{dataset}/{GUID}.[{format}?apikey={taxonomy_apikey}]'
    #save file as json
    file_name = f'{output_dir}/{dataset}_{GUID}.json'
    if response.status_code == 200:
        with open(file_name, 'x') as file:
            json.dump(response.json(), file)
    else:
        print(response.status_code)
