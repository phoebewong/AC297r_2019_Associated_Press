import requests
import json
import time
import constants
import urllib
from pathlib import Path

class ImageItem():
    '''
    A class for dealing with each image (1 association in the media API response for 1 article)
    '''
    def __init__(self, raw_json, full_json=None):
        self.raw_json = raw_json
        self.full_json_response = full_json

        if self.raw_json is None:
            assert(self.full_json_response is not None)
            self.itemid = self.full_json_response['data']['item']['altids']['itemid']
        else:
            self.itemid = self.raw_json['altids']['itemid']

        # creating a unique file so we don't lose data
        self.file_name = '{}/{}.json'.format(constants.IMAGE_DIR, self.itemid)
        self.thumbnail = '{}/{}.jpg'.format(constants.THUMBNAIL_DIR, self.itemid)

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

    def get_images(self, apikey):
        '''
        Saves image thumbnails in files
        '''
        # if a file exists, we don't call the API
        if Path(self.thumbnail).is_file():
            return

        # dealing with no renditions
        if 'renditions' not in self.full_json_response['data']['item'].keys():
            print('\n image {}: no renditions \n'.format(self.itemid))
            return

        # dealing with no thumbnail
        if 'thumbnail' not in self.full_json_response['data']['item']['renditions'].keys():
            print('\n image {}: no thumbnail \n'.format(self.itemid))
            return

        # getting the image file
        self.thumbnail_href = self.full_json_response['data']['item']['renditions']['thumbnail']['href']
        full_thumbnail_url = '{}&apikey={}'.format(self.thumbnail_href, apikey)
        urllib.request.urlretrieve(full_thumbnail_url, self.thumbnail)
        return
