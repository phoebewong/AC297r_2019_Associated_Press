import json
from src import constants
import os
import configparser
from image_item import ImageItem

if __name__ == '__main__':
    # Reading the password in
    config = configparser.ConfigParser()
    config.read('password.ini')
    apikey = (config['key']['apikey'])

    folder = '{}/image'.format(constants.DATA_DIR)

    # looking for all json files in our folder
    images = [file for file in os.listdir(folder) if file.endswith('.json')]

    # going through the files and saving the full text to file
    for i, file in enumerate(images):
        if i % 100 == 0:
            print('{} out of {} done'.format(i, len(images)))
        with open('{}/{}'.format(folder, file)) as json_file:
            json_data = json.load(json_file)
            image_item = ImageItem(raw_json=None, full_json=json_data).get_images(apikey)
