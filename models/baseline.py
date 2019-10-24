# baseline model
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet 
import string
from nltk.corpus import stopwords 

### FUNCTIONS ###

# utility functions
def clean_string(s):
    stop_words = set(stopwords.words('english')) 
    ret = list(set([x in s.translate(str.maketrans('', '', string.punctuation)).split() if x not in stop_words]))
    return ret

def clean_tags(tags):
    ts = []
    for t in tags:
        ts += t.split()
    return [x.lower() for x in ts]

# similarity metrics
def baseline_score(text, img):
    return len(set(text) & set(img['tags']))

def syn_score(text, img, eta=0.5):
    score = len(set(text) & set(img['tags']))
    for tag in text:
        for syn in wordnet.synsets(tag):
            for name in syn.lemma_names():
                if name in img['tags']:
                    score += eta
    return score

def tfidf_score(tfidf_df, text, img):
    ref = tfidf_df.loc[img['imgid'],:]
    score = 0
    for t in text:
        for i in img['tags']:
            if t == i:
                score += ref[i]
    return score
    

# baseline model
# ranks images based on tag overlap 
def baseline_model(text, images, n, score): 
    ranks = {} # top ten images 
    for img in images:
        s = score(text, img)
        if len(ranks) < n:
            ranks[len(ranks)] = (img['imgid'], s)
        elif s > min(ranks.values(), key=lambda x:x[1])[1]:
            key = min(ranks.keys(), key=lambda x:ranks[x][1])
            ranks[key] = (img['imgid'], s)
    return sorted(ranks.values(), key = lambda x:x[1], reverse=True)

### MAIN ###

if __name__ == "__main__":
    # test data
    # text_tags = ['General news', 'Government and politics', 'African-Americans', 'Race and ethnicity', 'Social issues', 'Social affairs', 'Racial and ethnic discrimination', 'Discrimination', 'Human rights and civil liberties'] # ['whale','dolphin']
    # text_tags = clean_tags(text_tags)
    text_tags = """South Africans along with former U.S. President Barack Obama were marking the centennial of anti-apartheid leader Nelson Mandela’s birth on Wednesday with acts of charity in a country still struggling with deep economic inequality 24 years after the end of white minority rule. Obama met with young leaders from around Africa to mark the anniversary, a day after he delivered a spirited speech in Johannesburg about Mandela’s legacy of tolerance and criticized President Donald Trump and his policies without mentioning him by name. An enthusiastic crowd of 14,000 gave Obama a standing ovation for his address, the highest-profile one since he left office. “Most people think of Mandela as an older man with hair like mine,” the 56-year-old, grey-haired Obama said to laughter from his audience on Wednesday. But he added that people forget that Mandela “started as a very young man, at your age, trying to liberate this country.” Speaking to participants in his Leaders Africa program, 200 young people from 44 African countries, he urged them to pursue change at home and emphasized the impact they can have as the continent’s population is the fastest-growing in the world. “How big are your ambitions?” he asked.
Obama also spoke out against the corruption and conflict that slow down change, mentioning as one example the current deadly tensions in Cameroon, which faces an Anglophone separatist movement and the threat from Boko Haram extremists based in neighboring Nigeria.
“Find a way where you’re not selling your soul,” Obama said, encouraging them to engage in political work and community involvement, especially women.
South Africans and others around the world marked the July 18, 1918 birth of Mandela with clinic openings, blanket handouts and other charitable acts. In Cape Town, numbers were painted on homes in one of the sprawling slums to help health workers locate people living with HIV and tuberculosis.
But South Africans must do more to fight for Mandela’s values daily instead of engaging in symbolic gestures on his birthday, main opposition leader Mmusi Maimane with the Democratic Alliance said, adding that South Africa’s “failed education is part of a system that locks black children out of opportunity.”
After 27 years in prison in South Africa, Mandela was released in 1990 and became the country’s first black president four years later. He died in 2013 at the age of 95.
Events have been planned throughout the year for the 100th anniversary of his birth, including a large concert in December in South Africa that will be headlined by Beyonce and Jay-Z and hosted by Oprah Winfrey and others.
In a video message, former South African archbishop Desmond Tutu said Mandela reflected the best of humanity.
“Good leaders make allowance for the fact that even they can be wrong, and they know when and how to say sorry. Madiba had this quality in abundance,” said Tutu, who was awarded the Nobel Peace Prize for his efforts to end apartheid and reconcile South Africans.
United Nations Secretary-General Antonio Guterres in a separate statement called Mandela a towering advocate for equality and justice.
“Nelson Mandela was held captive for many years. But he never became a prisoner of his past,” Guterres said. “Rarely has one person in history done so much to stir people’s dreams and move them to action.”"""
    text_tags = clean_string(text_tags)
    cap1 = "Children attend a special assembly to mark Mandela Day, at Melpark Primary School, in Johannesburg, Wednesday, July 18, 2018. South Africans along with former U.S. President Barack Obama are marking the centennial of Nelson Mandela's birth with acts of charity in a country still struggling with deep economic inequality 24 years after the end of white minority rule. (AP Photo/Denis Farrell)"
    cap2 = "Former US President Barack Obama speaks during his town hall for the Obama Foundation at the African Leadership Academy in Johannesburg, South Africa, Wednesday, July 18, 2018. (AP Photo/Themba Hadebe, Pool)"
    cap3 = "Children listen during a special assembly to mark Mandela Day, at Melpark Primary School, in Johannesburg, Wednesday, July 18, 2018. South Africans, along with former U.S. President Barack Obama, are marking the centennial of Nelson Mandela's birth with acts of charity in a country still struggling with deep economic inequality 24 years after the end of white minority rule. (AP Photo/Denis Farrell)"
    img1 = {'imgid':1,'tags':clean_string(cap1)}
    img2 = {'imgid':2,'tags':clean_string(cap2)}
    img3 = {'imgid':3,'tags':clean_string(cap3)}
    images = [img1,img2,img3] # test data = corpus of all available images

    # unit tests
    print('Simple Overlap Score:',baseline_model(text_tags, images, 3, baseline_score))
    print('Synonym + Overlap Score:',baseline_model(text_tags, images, 3, lambda x,y: syn_score(x,y,eta=0.5)))

    #tf-idf
    vectorizer = TfidfVectorizer()
    vecs = vectorizer.fit_transform([' '.join(i['tags']) for i in images])
    feats = vectorizer.get_feature_names()
    tfidf_df = pd.DataFrame(vecs.todense().tolist(), columns=feats)
    tfidf_df['label'] = [i['imgid'] for i in images]
    tfidf_df.set_index('label',inplace=True)
    print('TF-IDF Score:',baseline_model(text_tags, images, 3, lambda x,y: tfidf_score(tfidf_df,x,y)))

    # evaluation 