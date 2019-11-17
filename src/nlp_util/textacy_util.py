import textacy
import pandas as pd
from spacy.tokens import Doc
import numpy as np
import textacy.ke

en = textacy.load_spacy_lang("en_core_web_sm", disable=("parser",))

def get_textacy_name_entities(text, article_id, drop_determiners=True, exclude_types='numeric'):
    '''Get Named Entities using textacy
    text: full_text or summary
    article_id: string, article id (names of json files)
    Return a pd dataframe with two columns: named entities and entities category
    '''

    en = textacy.load_spacy_lang("en_core_web_sm", disable=("parser",))
    if isinstance(text, str): # if raw string
        doc = textacy.make_spacy_doc(text, lang=en)
    elif isinstance(text, Doc): # if pre-created spacy doc
        doc = text
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
    if article_id != None: # store article ID for csv
        data['article_id'] = article_id
    return data

def get_textrank_entities_only(textrank_words, textrank_score, entities_list, return_count=False):
    '''
    Return textrank results with only named entities
    Parameters:
    textrank_words: numpy array of textrank ngram tokens
    entities_list: list or numpy array of named entities extracted

    Return:
    A numpy array of textrank ngram tokens that contain named entities extracted
    '''
    ne_count = []
    entities_tr_score = []
    entities_scores = np.zeros(len(entities_list))
    entities_list = np.unique(entities_list)

    entities_output = []
    for rank_ix, textrank in enumerate(textrank_words): # for each textrank ngram token
        temp_score = 0
        for ix, entities in enumerate(entities_list): # for each named entities extracted
            if (entities in textrank):
                temp_score += 1
                entities_scores[ix] += 1
                entities_tr_score.append(textrank_score[rank_ix])
                entities_output.append(entities) # output named entities
            else:
                temp_score = temp_score
        # Counts of named entities in each text rank word
        ne_count.append(temp_score)
    textrank_score = np.array(textrank_score)
    if return_count:
        return textrank_words[np.array(ne_count) > 0], entities_tr_score, entities_output, entities_scores, np.array(ne_count)
    else:
        return textrank_words[np.array(ne_count) > 0], entities_tr_score, entities_output, entities_scores

def extract_textrank_from_text(text, textrank_topn = 0.99, textrank_window = 3, rel_gp = ['PERSON', 'GPE'],
                                use_spacy_entities = False, tagging_API_entities=None,
                                return_textrank_bags = False):
    '''
    A function for the full-cycle from input text to named entities text rank ngram tokens
    Parameters:
    doc: spacy Doc object, created with the input text
    textrank_topn: int, number of ngram tokens to be output from textrank
    textrank_window: int, ngram size of each textrank token
    rel_gp: list, a list of entities type to consider, default as person and geographic location
    use_spacy_entities: default False, True if wants to use spacy NER instead of tagging api
    tagging_API_entities: a numpy array of entities extracted from tagging API, only used when use_spacy_entities=False
    return_textrank_bags: default False, True if only wants to use textrank scores (and no entities)

    Return:
    textrank_entities: A numpy array of textrank ngram tokens that contain named entities extracted
    textrank_score: textrank importance score of textrank_entities (excluding those that do not contain named entities)
    entities_in_textrank: named entities that are included in the textrank bags
    '''
    # Create spacy object
    doc = textacy.make_spacy_doc(text, lang=en)
    # Get textrank keywords
    textrank_result = textacy.ke.textrank(doc, normalize="lemma", topn=textrank_topn, window_size=textrank_window)
    textrank_words, textrank_score = zip(*[(textrank[0], textrank[1]) for textrank in textrank_result])

    if return_textrank_bags:
        return textrank_words, textrank_score
    # Get named entities
    if use_spacy_entities:
        named_entities = get_textacy_name_entities(doc, article_id = None) # article id to be assigned to create the data
        # create a numpy array of unique entities from text
        entities_list = named_entities['text'][named_entities['label'].isin(rel_gp)].values
        entities_list = np.unique([entities.text for entities in entities_list])

    # else: # use tagging API
    else:
        entities_list = tagging_API_entities
    # Textrank ngram keywords that has >=1 named entities
    textrank_entities, textrank_score, entities_output, entities_scores, ne_count = get_textrank_entities_only(np.array(textrank_words), textrank_score, entities_list, return_count=True)
    # 0 or 1 if the entities is included in textrank
    entities_scores = np.array(list(map(int, entities_scores)))
    # Average out textrank score for entities that are in >=1 textrank bags of words
    temp_df = pd.DataFrame([textrank_score, list(entities_output)]).T.rename(columns = \
              {0:"TextRank_score", 1:"named_entities"})
    temp_df.TextRank_score = temp_df.TextRank_score.astype(float)
    # Get average textrank score per entity and sort the df in descending order
    temp_df2 = temp_df.groupby('named_entities').mean().sort_values(by = 'TextRank_score', ascending=False).reset_index()
    textrank_score = temp_df2['TextRank_score'].values
    entities_output = temp_df2['named_entities'].values
    # Return named entities extracted that existed in textrank keywords
    # entities_in_textrank = np.unique(entities_list)[entities_scores >= 1]

    return textrank_entities, np.round(textrank_score, 5), entities_output
