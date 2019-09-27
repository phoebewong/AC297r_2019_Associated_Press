import requests
import json
import time
from image_item import ImageItem

class ArticleItem():
    '''
    A class for dealing with each article (1 item in the media API response)
    '''
    def __init__(self, apikey, raw_json):
        self.apikey = apikey
        self.raw_json = raw_json
        self.full_json_response = None
        self.itemid = self.raw_json['altids']['itemid']
        self.full_json_response = self.get_full_json_response()

    def get_full_json_response(self, itemid=None):
        '''
        Goes to the article uri and gets the full json response
        '''
        try:
            # see if we have already saved a file with this item id
            return self.get_full_json_response_file()
        except:
            # no file saved, doing an API request
            pass

        full_url = '{}&apikey={}'.format(self.get_uri(), self.apikey)
        self.response = requests.get(full_url)
        # creating a unique file so we don't lose data
        self.file_name = '../../data/article/{}.json'.format(self.itemid)

        # write to json file if the response is ok
        if self.response.status_code == 200:
            with open(self.file_name, 'x') as outfile:
                self.full_json_response = self.response.json()
                json.dump(self.full_json_response, outfile)
        return self.full_json_response

    def get_filename_from_itemid(self):
        '''
        Helper function that uses saved json files for that article if they exist
        '''
        return '../../data/article/{}.json'.format(self.itemid)

    def get_full_json_response_file(self):
        '''
        Helper function to load json if we have already saved a file corresponding to this article
        '''
        file_name = self.get_filename_from_itemid()
        try:
            with open(file_name, 'r') as infile:
                self.full_json_response = json.load(infile)
                return self.full_json_response
        except FileNotFoundError:
            raise

    def get_headline(self):
        return self.raw_json['headline']

    def get_uri(self):
        return self.raw_json['uri']

    def get_entities(self):
        '''
        Gets all entities from an article item.
        The list of entities from the article seem to be:
        '''
        entities_list = ['person', 'subject', 'organisation', 'place', 'event']
        people = self.full_json_response['data']['item']['place']
        entities_dict = {}
        for entity in entities_list:
            if entity not in self.full_json_response['data']['item'].keys():
                continue
            list_of_tags = self.full_json_response['data']['item'][entity]
            entities_dict[entity] = []
            for tag in list_of_tags:
                if tag['name'] is not None:
                    entities_dict[entity].append(tag['name'])
        return entities_dict

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
            association = ImageItem(self.apikey, association_raw)
            return association
        else:
            return None

    def get_text(self):
        '''
        TODO: figure out how to get full text
        '''
        raise NotImplementedError
