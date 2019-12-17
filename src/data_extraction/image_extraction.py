import json
from src import constants
import os
import configparser
import time, datetime
from image_item import ImageItem

if __name__ == '__main__':
    # Reading the password in
    config = configparser.ConfigParser()
    config.read('password.ini')
    apikey = (config['key']['apikey'])

    folder = '{}/image'.format(constants.DATA_DIR)

    # looking for all json files in our folder
    images = [file for file in os.listdir(folder) if file.endswith('.json')]
    start_time = time.time()

    # going through the files and saving the full text to file
    for i, file in enumerate(images):
        if i % 10000 == 0:
            now = datetime.datetime.now().time()
            print('{} out of {} done. time: {}. elapsed: {}s'.format(i, len(images), now, int(time.time() - start_time)))
        with open('{}/{}'.format(folder, file)) as json_file:
            json_data = json.load(json_file)

            # get previews: comment out this line if you don't want them
            image_item = ImageItem(raw_json=None, full_json=json_data).get_image_previews(apikey)

            # get thumbnails: comment out this line if you don't want them
            image_item = ImageItem(raw_json=None, full_json=json_data).get_image_thumbnails(apikey)

            # check if the preview/thumbnail path exists. if not it prints out the id
            image_item = ImageItem(raw_json=None, full_json=json_data).check_thumbnail_previews()
