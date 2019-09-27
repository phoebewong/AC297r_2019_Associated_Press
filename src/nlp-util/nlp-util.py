import spacy
import pandas as pd

def get_name_entity(doc, labels = None):
    """
    Return a dataframe of name entity when given a spacy doc of text
    Inputs:
    doc -- a spaCy doc
    labels -- optional, a list of entity labels to include in the result


    Return:
    A dataframe with two columns, one is the original text and two is the identified label
    """
    if labels != None:
        text = list(map(lambda x: x.text, doc.ents)) # entity text
        label = list(map(lambda x: x.label_, doc.ents)) # entity labels
        data = pd.DataFrame(data = {'text': text,
                     'label': label})

    else:
        text = list(map(lambda x: x.text, doc.ents)) # entity text
        label = list(map(lambda x: x.label_, doc.ents)) # entity labels
        data = pd.DataFrame(data = {'text': text,
                     'label': label})
        data = data[data['label'].isin(labels)] # filter out rows that include specified labels
    return data
