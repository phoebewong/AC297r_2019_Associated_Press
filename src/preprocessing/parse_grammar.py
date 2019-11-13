#dependencies
import os
import pandas as pd
import numpy as np
from src import constants
from nltk.tree import Tree, ParentedTree
from nltk.parse import stanford
from nltk.corpus import wordnet as wn
import process_utils

#set environment variables to access stanford parser
os.environ['CLASSPATH'] = str(constants.STANFORD_PARSER)
os.environ['STANFORD_MODELS'] = str(constants.STANFORD_PARSER)

#initiate stanford parser
parser = stanford.StanfordParser()

def pp(sentences):
    '''
    retrieve list of prepositional phrases in tree.

    Params:
    -------
    1) sentences: list or array-like, sentences to process

    Return:
    -------
    list of prepositional phrases
    '''
    parsed_sentence = parser.raw_parse_sents((sentences))
    #cache list to record all prepositional phrases
    pp_phrases = list()
    for object in parsed_sentence:
        for sentence in object:
            pp = list()
            #retrieve all subtrees starting with PP
            for i in sentence.subtrees(filter = lambda x: x.label() == 'PP'):
                pp.extend(i.leaves())
            pp_phrases.append(pp)
    return pp_phrases

def get_scene_factors(pps, tags):
    "get scene factor given prepositional phrases and target scene tags"
    sfs = [1 if tags[i] in pps[i] else 2 for i in range(len(tags))]
    return np.array(sfs)

def get_synonyms(phrase):
    "get set of synonyms using wordnet"
    syns = list()
    if ' ' in phrase:
        #concatenate phrases if applies
        phrase = phrase.replace(' ', '_')
    synsets = wn.synsets(phrase)
    for s in synsets:
        if '.n.' in s.name():
            syns.extend(s.lemma_names())
    unique = list(set(syns))
    unique = [x.replace('_', ' ').lower() for x in unique]
    return unique
