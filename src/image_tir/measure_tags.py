#dependencies
import sys
from src import constants
sys.path.append(str(constants.PREPROCESSING_DIR))
import parse_grammar
import process_utils
import numpy as np
import pandas as pd
from collections import defaultdict
from nltk.corpus import wordnet

#data directory path
data_directory = constants.CLEAN_DIR
img_prefix = constants.Media_Prefix

class MeasureTag:
    "measure image tag importances"
    def __init__(self, idx, st_types, ot_types):
        self.idx = idx #image id
        self.scene_tag_types = st_types #list of scene tag types, csv suffix
        self.object_tag_types = ot_types #list of object tag types, csv suffix
        #attributes to update
        self.scene_tags = None
        self.object_tags = None
        self.descriptions = None
        self.st_importance = None
        self.ot_importance = None
        self.pps = None
        self.sf_weights = None
        self.num_sts = None

    def get_tags(self, tag_types):
        '''
        search thru tag type file and retrieve scene tags.

        Params:
        -------
        1) tag_types: list or array-like, csv files to search through

        Return:
        -------
        retrieve object / scene tags
        '''
        search_tags = list()
        for tag in tag_types:
            file_path = f'{data_directory}/{img_prefix}{tag}.csv'
            data = pd.read_csv(file_path)
            try:
                #subset for image
                subset = data[data.id == self.idx]
                tags = subset[f'{tag}_tag'].values
                for t in tags:
                    #check validity of tag
                    if process_utils.if_valid(t):
                        #format string and record
                        search_tags.append(t.lower().replace(',', ''))
            except:
                continue
        #retrieve tags
        return search_tags

    def get_descriptions(self):
        "get list of descriptions for given image"
        if self.descriptions is None:
            descriptions = list()
            file_path = f'{data_directory}/{img_prefix}summary.csv'
            summary_data = pd.read_csv(file_path)
            subset = summary_data[summary_data.id == self.idx]
            for value in ['title', 'headline', 'headline_extended', 'summary']:
                d = subset[value].values[0]
                if process_utils.if_valid(d):
                    #break into sentences
                    dvec = [d.lower() for d in process_utils.get_sentence(d)]
                    descriptions.extend(dvec)
            self.descriptions = descriptions
            #update list of preopositional phrases
            self.pps = parse_grammar.pp(self.descriptions)

    def get_st_importance(self):
        "get scene tag importance"
        if self.scene_tags is None:
            self.scene_tags = self.get_tags(self.scene_tag_types)

        importance = defaultdict(float)
        #scene factor weights for object tag computation
        record_weights = 1
        #number of scene factor per description for object tag computation
        record_sts = 0
        for tag in self.scene_tags:
            #get synonym for tag
            syns = parse_grammar.get_synonyms(tag)
            #replace tag with synonym if applies
            replace_tags = [[x in s for x in syns][0] if [x in s for x in syns][0] else tag for s in self.descriptions]
            #indicator vector
            i_tag = np.array([1 if any(item in s for item in syns) else 0 for s in self.descriptions])
            #update number of scene factor per description
            record_sts += i_tag
            #get scene factor weight
            css = parse_grammar.get_scene_factors(self.pps, replace_tags)
            #mute tag that doesn't exist in sentence
            cs_vec = i_tag * css
            #updating weights for object tag computation : 1+cs
            update_weights = np.array([1 if i_tag[m] == 0 else 1+css[m] for m in range(len(i_tag))])
            record_weights *= update_weights
            #average scene tag across descriptions
            imp = np.mean(cs_vec/(1+cs_vec))
            importance[tag] = imp

        self.st_importance = dict(importance)
        self.sf_weights = record_weights
        self.num_sts = record_sts

    def get_ot_importance(self):
        "get object tag importances"
        if self.scene_tags is None:
            self.scene_tags = self.get_tags(self.scene_tag_types)
        if self.object_tags is None:
            self.object_tags = self.get_tags(self.object_tag_types)

        if len(self.object_tags) == 0:
            self.ot_importance = dict()
        else:
            importance = defaultdict(float)
            #set of all object tags in sentence
            ot_set = [[ot for ot in self.object_tags if ot in s] for s in self.descriptions]
            #number of object tags
            num_ots = np.array([len(ot) for ot in ot_set])

            for tag in self.object_tags:
                #numpy ignore division by 0 error
                #when description contains 0 object tags
                np.seterr(divide='ignore', invalid='ignore')
                #indicator vector, whether object tag exist in description
                i_vec = np.array([1 if tag in s else 0 for s in self.descriptions])
                #average object tag weights across total number of descriptions
                imp = np.nansum(np.divide(i_vec, (num_ots**self.num_sts)*self.sf_weights)) / len(self.descriptions)
                importance[tag] = imp
            self.ot_importance = dict(importance)
