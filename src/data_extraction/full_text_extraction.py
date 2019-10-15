import json
import constants
import os
import configparser
from article_item import ArticleItem

if __name__ == '__main__':
    # Reading the password in
    config = configparser.ConfigParser()
    config.read('password.ini')
    apikey = (config['key']['apikey'])

    folder = '{}/article'.format(constants.DATA_DIR)

    # looking for all json files in our folder
    articles = [file for file in os.listdir(folder) if file.endswith('.json')]

    # going through the files and saving the full text to file
    for i, file in enumerate(articles):
        if i%100 == 0:
            print('{} out of {} done'.format(i, len(articles)))
        with open('{}/{}'.format(folder, file)) as json_file:
            json_data = json.load(json_file)
            article_item = ArticleItem(raw_json=None, full_json=json_data).get_text(apikey)
