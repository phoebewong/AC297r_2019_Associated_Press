import textacy
import pandas as pd
from spacy.tokens import Doc
import numpy as np

def get_textacy_name_entities(text, article_id, drop_determiners=True, exclude_types='numeric'):
    '''Get Named Entities using textacy
    text: full_text or summary
    article_id: string, article id (names of json files)

    Return a pd dataframe with two columns: named entities and entities category
    '''

    en = textacy.load_spacy_lang("en_core_web_sm", disable=("parser",))
    if isinstance(text, str):
        doc = textacy.make_spacy_doc(text, lang=en)
    elif isinstance(text, Doc): # if pre-created spacy doc
        doc = doc
    else:
        doc = textacy.make_spacy_doc("NA", lang=en)

    nes = textacy.extract.entities(doc, drop_determiners=drop_determiners, exclude_types=exclude_types) # nes is a generator
    ne_list = []
    ne_label_list = []

    for ne in nes:
        ne_list.append(ne)
        ne_label_list.append(ne.label_)

    data = pd.DataFrame(data = {'text': ne_list, 'label': ne_label_list})
    ## TODO: CHECK why drop_duplicate is not working ##
    data = data.drop_duplicates(keep='first')
    data['article_id'] = article_id
    return data

def get_textrank_entities_only(textrank_words, entities_list, return_count=False):
    '''
    Return textrank results with only named entities
    Parameters:
    textrank_words: numpy array of textrank ngram tokens
    entities_list: list or numpy array of named entities extracted

    Return:
    A numpy array of textrank ngram tokens that contain named entities extracted
    '''
    ne_count = []

    for textrank in textrank_words: # for each textrank ngram token
        temp_score = 0
        for entities in entities_list: # for each named entities extracted
            if (entities in textrank):
                temp_score +=1
            else:
                temp_score = temp_score
        # Counts of named entities in each text rank word
        ne_count.append(temp_score)

    if return_count:
        return textrank_words[np.array(ne_count) > 0], counts
    else:
        return textrank_words[np.array(ne_count) > 0]
