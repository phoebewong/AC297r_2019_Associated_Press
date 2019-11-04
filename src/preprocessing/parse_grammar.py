#dependencies
import os
from src import constants
from nltk.tree import Tree, ParentedTree
from nltk.parse import stanford

#set environment variables to access stanford parser
os.environ['CLASSPATH'] = str(constants.STANFORD_PARSER)
os.environ['STANFORD_MODELS'] = str(constants.STANFORD_PARSER)

#initiate stanford parser
parser = stanford.StanfordParser()

def if_pp(sentence, tag):
    "check whether scene tag exists as prepositional phrase in sentence"
    parsed_sentence = parser.raw_parse((sentence))
    #cache list to record all prepositional phrases
    pp_phrases = list()
    for object in parsed_sentence:
        for sentence in object:
            #retrieve all subtrees starting with PP
            for i in sentence.subtrees(filter = lambda x: x.label() == 'PP'):
                pp_phrases.extend(i.leaves())
    if tag in pp_phrases:
        return True
    else:
        return False
