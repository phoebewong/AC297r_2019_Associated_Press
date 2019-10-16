import textacy
import pandas as pd


def get_textacy_name_entities(text, article_id, drop_determiners=True, exclude_types='numeric'):
    '''Get Named Entities using textacy
    text: full_text or summary
    article_id: string, article id (names of json files)

    Return a pd dataframe with two columns: named entities and entities category
    '''

    en = textacy.load_spacy_lang("en_core_web_sm", disable=("parser",))
    if isinstance(text, str):
        doc = textacy.make_spacy_doc(text, lang=en)
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
