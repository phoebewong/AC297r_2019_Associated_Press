import requests
import json
import time
from image_item import ImageItem
import constants

class ArticleItem():
    '''
    A class for dealing with each article (1 item in the media API response)
    '''
    def __init__(self, raw_json):
        self.raw_json = raw_json
        self.full_json_response = None
        self.itemid = self.raw_json['altids']['itemid']
        self.full_json_response = None
        # creating a unique file so we don't lose data
        self.path = constants.DATA_DIR
        self.file_name = '{}/article/{}.json'.format(self.path, self.itemid)

    def save_full_json_response(self, apikey, itemid=None):
        '''
        Goes to the article uri and gets the full json response
        '''
        try:
            # see if we have already saved a file with this item id
            return self.get_full_json_response_file()
        except:
            # no file saved, doing an API request
            pass

        full_url = '{}&apikey={}'.format(self.get_uri(), apikey)
        self.response = requests.get(full_url)

        # write to json file if the response is ok
        if self.response.status_code == 200:
            with open(self.file_name, 'x') as outfile:
                self.full_json_response = self.response.json()
                json.dump(self.full_json_response, outfile)
        return self.full_json_response

    def get_full_json_response_file(self):
        '''
        Helper function to load json if we have already saved a file corresponding to this article
        '''
        try:
            with open(self.file_name, 'r') as infile:
                self.full_json_response = json.load(infile)
                return self.full_json_response
        except FileNotFoundError:
            raise

    def get_uri(self):
        return self.raw_json['uri']

    def get_associations(self):
        '''
        Gets all the associations (images) from the article item.
        '''
        try:
            return self.full_json_response['data']['item']['associations']
        except:
            return None

    def get_association_count(self):
        '''
        Gets the count of how many associations there are in the json output
        '''
        return len(self.full_json_response['data']['item']['associations'])

    def get_specific_association(self, association_key):
        '''
        Gets a specific association (image) from the list of images
        '''
        if association_key in self.full_json_response['data']['item']['associations'].keys():
            association_raw = self.full_json_response['data']['item']['associations'][association_key]
            association = ImageItem(association_raw)
            return association
        else:
            return None

    def get_text(self):
        '''
        TODO: figure out how to get full text
        '''
        raise NotImplementedError
