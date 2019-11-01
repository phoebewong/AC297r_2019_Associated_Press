###extract taxonomy datasets

import json
import requests
from src import constants
import configparser

output_dir = constants.TAXONOMY_DIR

if __name__ == '__main__':

    #retrieve password
    config = configparser.ConfigParser()
    config.read('password.ini')
    taxonomy_apikey =  (config['key']['apikey'])

    #available taxonomy dataset for call
    datasets = ['subject', 'geography', 'organization', 'person']

    for data in datasets:
        request_url = f'http://cv.ap.org/d/{data}.json?apikey={taxonomy_apikey}'
        response = requests.get(request_url)
        #json file name
        file_name = f'{output_dir}/taxonomy_{data}.json'
        if response.status_code == 200:
            with open(file_name, 'x') as file:
                json.dump(response.json(), file)
        else:
            print(response.status_code)
