import requests
import json
import time
import constants

class ImageItem():
    '''
    A class for dealing with each image (1 association in the media API response for 1 article)
    '''
    def __init__(self, raw_json):
        self.raw_json = raw_json
        self.full_json_response = None
        self.itemid = self.raw_json['altids']['itemid']
        self.full_json_response = None
        # creating a unique file so we don't lose data
        self.path = constants.DATA_DIR
        self.file_name = '{}/image/{}.json'.format(self.path, self.itemid)

    def save_full_json_response(self, apikey, associationid=None):
        '''
        Goes to the image uri and gets the full json response
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
        Helper function to load json if we have already saved a file corresponding to this image
        '''
        try:
            with open(self.file_name, 'r') as infile:
                self.full_json_response = json.load(infile)
                return self.full_json_response
        except FileNotFoundError:
            raise

    def get_uri(self):
        '''
        Helper function to get uri
        '''
        return self.raw_json['uri']
