import requests
import json
import time

class ImageItem():
    '''
    A class for dealing with each image (1 association in the media API response for 1 article)
    '''
    def __init__(self, apikey):
        self.apikey = apikey
