import pandas as pd
import numpy as np
from src import constants

def random_article_extractor():
    """
    Gets the text and body of a random article in our dataset
    """
    csv_file = constants.CLEAN_DIR / 'article_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'headline', 'full_text']]
    ind = np.random.choice(range(len(subset)))

    id = subset['id'].values[ind]
    title = subset['headline'].values[ind]
    body = subset['full_text'].values[ind]
    return id, title, body

def article_id_extractor(title, body):
    """
    If a title and body is in our dataset, we return its corresponding id
    """
    csv_file = constants.CLEAN_DIR / 'article_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'headline']]
    try:
        return subset[subset['headline'] == title]['id'].values[0]
    except:
        return None

def article_images(id):
    """
    Gets all the images for a particular article id
    """
    csv_file = constants.CLEAN_DIR / 'image_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'article_idx']]
    images = subset[subset['article_idx'] == id]['id'].values
    return images

def image_captions(ids):
    """
    Gets the image caption for an image
    """
    csv_file = constants.CLEAN_DIR / 'image_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'headline']]
    captions = []
    for id in ids:
        try:
            caption = subset[subset['id'] == id]['headline'].values[0]
        except:
            caption = 'No Caption'
        captions.append(caption)
    return captions

def tagging_api(title, body):
    """
    Tags articles (at the moment it gets tags from the dataset)
    """
    id = article_id_extractor(title, body)
    if id == None:
        return None

    art_sub = pd.read_csv(constants.CLEAN_DIR / 'article_subject.csv')
    art_person = pd.read_csv(constants.CLEAN_DIR / 'article_person.csv')
    art_place = pd.read_csv(constants.CLEAN_DIR / 'article_place.csv')
    art_org = pd.read_csv(constants.CLEAN_DIR / 'article_org.csv')

    art_sub['type'] = 'subject'
    art_person['type'] = 'person'
    art_place['type'] = 'place'
    art_org['type'] = 'org'

    art_sub = art_sub[art_sub['id'] == id][['subject_tag', 'type']].dropna(axis=0)
    art_sub = art_sub.rename(columns={"subject_tag": "tag"})

    art_person = art_person[art_person['id'] == id][['person_tag', 'type']].dropna(axis=0)
    art_person = art_person.rename(columns={"person_tag": "tag"})

    art_place = art_place[art_place['id'] == id][['place_tag', 'type']].dropna(axis=0)
    art_place = art_place.rename(columns={"place_tag": "tag"})

    art_org = art_org[art_org['id'] == id][['org_tag', 'type']].dropna(axis=0)
    art_org = art_org.rename(columns={"org_tag": "tag"})

    art_alltags = pd.concat([art_sub, art_person, art_place, art_org])

    return id, art_alltags['tag'].values, art_alltags['type'].values

def matching_articles(ids):
    """
    Matching articles and getting headlines
    """
    csv_file = constants.CLEAN_DIR / 'article_summary.csv'
    data = pd.read_csv(csv_file)
    subset = data[['id', 'headline']].dropna(axis=0)
    headlines = []
    for id in ids:
        try:
            headlines.append({'id': id, 'headline': subset[subset['id'] == id]['headline'].values[0]})
        except:
            headlines.append({'id': id, 'headline': 'no headline found: {}'.format(id)})
            
    return headlines

def postprocess(x):
    """
    Post-processes output of models so we can predict images (using indices)
    """
    csv_file = constants.CLEAN_DIR / 'image_person.csv'
    data = pd.read_csv(csv_file)
    indices = [idx%len(data) for idx in x.flatten()]
    return np.array(data.iloc[indices].id).reshape(-1,1)

if __name__ == '__main__':
    headline = "Gdansk mayor: No public space for divisive priest's statue"
    full_text = "WARSAW, Poland (AP) — The new mayor of the Polish city of Gdansk says a statue of late Solidarity-era priest Henryk Jankowski, at the center of allegations he abused minors, should not stand in a public place.The statue recognizes Jankowski's staunch support for the Solidarity pro-democracy movement in the 1980s, born out of Gdansk shipyard workers' protest.But the abuse allegations led three men to overturn it one night last month. Shipyard workers put it back up.Mayor Aleksandra Dulkiewicz said late Monday both actions were illegal and hampered peaceful dialogue about the monument's future. She said the statue should stand on private property, without specifying. It could mean church land.On Thursday, Gdansk councilors are to debate whether to dismantle the statue."

    headline = "Brexiteer Farage splattered in latest UK milkshake attack"
    full_text = "LONDON (AP) — Pro-Brexit British politician Nigel Farage was hit with a milkshake while campaigning in the European Parliament election on Monday — the latest in a spate of attacks on politicians with the sticky beverages.Farage was left with milkshake dripping down his lapels during a walkabout in Newcastle, northeast England. Police said a 32-year-old man was arrested on suspicion of assault.Paul Crowther, who was detained in handcuffs at the scene, said he threw the banana-and-salted caramel Five Guys shake to protest Farage's 'bile and racism.' He said he had been looking forward to the milkshake, 'but I think it went on a better purpose.' Farage blamed the attack on those who wanted to remain in the EU. He tweeted that 'Sadly some remainers have become radicalised, to the extent that normal campaigning is becoming impossible.' Farage's Brexit Party is leading opinion polls in the contest for 73 U.K. seats in the 751-seat European Parliament.Milkshakes have become an unlikely political weapon in Britain. Other right-wing candidates including far-right activist Tommy Robinson have also been pelted with milkshakes during the election campaign.Last week a McDonald's in Edinburgh, Scotland said it had been told by police not to sell milkshakes during a Brexit Party rally.In response, Burger King tweeted: 'Dear people of Scotland. We're selling milkshakes all weekend. Have fun. Love BK.'"

    bad_id = "c3c12c99cf644aafa0c830c9c047ca9b"

    id, all_tags, tag_types = tagging_api(headline, full_text)
    print(id)
    print(all_tags)
    images = article_images(id)
    print(images)
    captions = image_captions(images)
    print(captions)
