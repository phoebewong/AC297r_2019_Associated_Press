import requests
import json
import time
from article_item import ArticleItem
import constants

class MediaItem:
    '''
    A class for making requests to the media API and saving the responses as json
    '''
    def __init__(self, page_size=100, qt=None):
        self.url = 'https://api.ap.org/media'
        self.page_size=page_size
        self.qt = qt
        self.json_response = None
        self.response = None
        self.file_name = None

    def make_get_request(self, apikey):
        '''
        Makes a get request. If the request is ok, a json file is saved with the response
        '''
        # URL format: https://api.ap.org/media/content/ondemand?qt={}&apikey={apikey}[{optional_parameters}]
        if self.qt is None:
            self.full_url = '{}/content/ondemand?apikey={}&page_size={}'.format(self.url, apikey, self.page_size)
        else:
            self.full_url = '{}/content/ondemand?qt={}&apikey={}&page_size={}'.format(self.url, self.qt, apikey, self.page_size)
        self.response = requests.get(self.full_url)

        # creating a unique file so we don't lose data
        self.file_name = '{}/full/{}.json'.format(constants.DATA_DIR, int(time.time()))

        # write to json file if the response is ok
        if self.response.status_code == 200:
            with open(self.file_name, 'x') as outfile:
                self.json_response = self.response.json()
                json.dump(self.json_response, outfile)
        return self.response

    def get_json_response(self):
        '''
        Call this function after making a request
        '''
        return self.json_response

    def get_json_response_from_file(self, file_name):
        '''
        Read json from a file
        '''
        with open(file_name, 'r') as infile:
            self.json_response = json.load(infile)
        return self.json_response

    def get_item_count(self):
        '''
        Gets the count of how many items there are in the json output
        '''
        return len(self.json_response['data']['items'])

    def get_items(self):
        '''
        Gets all items in the json response
        '''
        try:
            return self.json_response['data']['items']
        except:
            return None

    def get_specific_item(self, item_index):
        '''
        Return is of type ArticleItem
        '''
        if item_index < self.get_item_count():
            item_raw = self.json_response['data']['items'][item_index]['item']
            item = ArticleItem(item_raw)
            return item
        else:
            return None
