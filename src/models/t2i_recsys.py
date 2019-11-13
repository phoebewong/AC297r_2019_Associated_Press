import json
from src import constants

#directory path
data_directory = constants.DATA_DIR
#update this in constants.py now
obj_imp_filename = 'object_tag_importance_all.json'
scn_imp_filename = 'scene_tag_importance_all.json'

class T2I:
    "class function for tag-to-image recommendation"
    def __init__(self, tags):
        self.tags = tags #tags used in recommendation search
        
