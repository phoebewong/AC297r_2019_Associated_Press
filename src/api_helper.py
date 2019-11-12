import pandas as pd
import numpy as np
from src import constants

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
            headlines.append('id: {}. headline: {}'.format(id, subset[subset['id'] == id]['headline'].values[0]))
        except:
            headlines.append('id: {}. headline: none'.format(id))
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
    # ids = ['0141bc4aee7c4352a242a8138135f9be', '00d713a2b6cb44c88fbd2fd3f10228f3', '00c6682106da42f299ab9955de385aa5']
    # print(matching_articles(ids))

    # 1
    headline = "Walmart partners with Google on grocery shopping via voice"
    full_text = "Walmart will now be allowing its shoppers to order their groceries by voice through Google's smart home assistant, its latest attempt to challenge Amazon's growing dominance","NEW YORK (AP) — Walmart will now allow its shoppers to order their groceries by voice through Google's smart home assistant, its latest attempt to challenge Amazon's growing dominance.Starting this month, shoppers can add items directly to their Walmart grocery cart, according to a company blog post on Tuesday. Walmart Inc. says it can quickly identify the items customers are asking for, based on information from prior purchases with Walmart. For example, if a customer tells Google Assistant to add milk to the cart, it can make sure to add the specific milk the customer buys regularly.The new features come almost two years after the retailer announced a partnership with Google.Amazon.com's Echo will capture 63.3% of smart speaker users in 2019, while Google Home will account for 31%, according to eMarketer."

    # 2
    headline = "Clashes mar peaceful protests as Algerians march anew"
    full_text = "ALGIERS, Algeria (AP) — Police fired intense volleys of tear gas and used water cannons in clashes in the Algerian capital during the eighth week of massive Friday demonstrations that forced the president to resign and now aim to rid the nation of its interim leadership.Police arrested 108 people in the confrontations in Algiers, the capital, in which 27 officers were injured, police said, adding that four of the officers were in serious condition. No mention was made of civilians.The clashes were between police and ""delinquents infiltrated"" into the protests, the reliable online publication TSA Algerie reported, citing the General Direction for National Security, known as the DGSN.In an earlier statement, the DGSN said security forces arrested foreigners trying to raise tensions and push youth into ""forms of radical expression"" during protest marches. It did not say who or how many had been detained.The statement also said that through the weeks of protests delinquents and others have been arrested among demonstrators with some trying to steal, harass or be aggressive, the official APS news agency reported.The Algiers clashes tainted what have been peaceful nationwide protests that have been a source of pride for the North African nation whose population is trying to do away with the political system that has prevailed since independence from France in 1962.Abdelaziz Bouteflika was forced to resign April 2, pressured by protests that began Feb. 22, and clinched when the powerful army chief firmly reiterated the demand.Friday's protests were the first since the interim leader, Abdelkader Bensalah, announced this week the date for presidential elections — July 4.""Everybody get out,"" protesters chanted, reflecting the demand that the former president's entourage, widely viewed as corrupt, leave, and their dream of a new Algeria.Tension mounted in late afternoon when some protesters tossed rocks and bottles at police at a small square that serves as a key point for gatherings. Police moved in with tear gas. An Associated Press photographer saw an officer firing what apparently were rubber bullets.Security forces then went after crowds with tear gas at key points around the city center where protesters gather, including the iconic central post office, the main gathering point for the pro-democracy movement. Two helicopters flew above the acrid smoke that sent crowds running.When tear gas was fired at protesters at the junction of a boulevard and a road leading to the president's office, cries of ""Allaoh akbar"" and ""Peaceful! Peaceful!"" were heard. Volleys of tear gas then targeted another main axis through the city center and eventually moved to the post office.The streets were packed with protesters waving Algerian flags. Some shouted ""Authorities - Assassins!"" and surrounded a water cannon truck, with some appearing to hit it.Much of the anger was focused on the interim president, Bensalah, seen as a remnant of the old regime.""Bensalah, get out!"" the protesters shouted, as a river of people adorned in green, white and red Algerian flags wove through the city.""His Majesty the People orders you to resign tomorrow!"" read one sign. Another called Bensalah, and the prime minister and the constitutional council president ""Residue of the Bouteflika System.""Anger is also mounting at military chief Gen. Ahmed Gaid Salah, who was instrumental in Bouteflika's departure but then threw his support behind Bensalah.Protesters called for a truly independent leadership structure and a technocratic government to lead a political transition.""It's been eight weeks since I've seen my family, I'm so tired,"" said one police officer, Salim, as he choked back tears. The 32-year-old spoke to The AP on condition his last name not be used for fear of repercussions. ""I never thought I'd find myself confronting my compatriots to stop them from protesting. They're my age.""Algeria's protest movement has been driven by young people frustrated with corruption and unemployment and who want a new generation of leaders.""Mentalities have to change. It's not just about going out and shouting, which is good and important, but taking action is important too,"" said Imad Touji, a 22-year-old student.""We really need to change things in a concrete way.""___Mosa'ab Elshamy in Algiers contributed."

    # 3
    headline = "Turkey: 9 detained in opposition leader's assault at funeral"
    full_text = "Turkey's interior minister says nine people have been detained in the assault of an opposition party leader, who was hit during a soldier's funeral","Turkey's interior minister says nine people have been detained in the assault of an opposition party leader, who was hit during a soldier's funeral. Several protesters threw punches at Republican People's Party leader Kemal Kilicdaroglu at the funeral outside Ankara on Sunday. Kilicdaroglu was not injured.","ANKARA, Turkey (AP) — Turkey's interior minister says nine people have been detained in the assault of an opposition party leader, who was hit during a soldier's funeral.Several protesters threw punches at Republican People's Party leader Kemal Kilicdaroglu at the funeral outside Ankara on Sunday. Kilicdaroglu was not injured.Interior Minister Suleyman Soylu said Monday nine people were detained for questioning.The soldier was killed Saturday in clashes with Kurdish rebels. Soylu appeared to justify Kilicdaroglu's assault by referring to the support a pro-Kurdish gave the opposition during Turkey's March 31 municipal elections.Soylu said: ""Everyone must take sides against the (rebels).""The Republican People's Party won the mayoral elections in Ankara and Istanbul, supplanting President Recep Tayyip Erdogan's party.Erdogan led a divisive campaign, equating opposition parties with terrorists."

    id, all_tags, tag_types = tagging_api(headline, full_text)
    print(id)
    print(all_tags)
    images = article_images(id)
    print(images)
