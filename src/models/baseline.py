# baseline model
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet

### FUNCTIONS ###

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
    text_tags = ['whale','dolphin']
    img1 = {'imgid':1,'tags':['whale','dolphin']}
    img2 = {'imgid':2,'tags':['whale','sea']}
    img3 = {'imgid':3,'tags':['sea','wave']}
    images = [img2, img3, img1]

    # unit tests
    print('Simple Overlap Score:',baseline_model(text_tags, images, 2, baseline_score))
    print('Synonym + Overlap Score:',baseline_model(text_tags, images, 2, lambda x,y: syn_score(x,y,eta=0.5)))

    #tf-idf
    vectorizer = TfidfVectorizer()
    vecs = vectorizer.fit_transform([' '.join(i['tags']) for i in images])
    feats = vectorizer.get_feature_names()
    tfidf_df = pd.DataFrame(vecs.todense().tolist(), columns=feats)
    tfidf_df['label'] = [i['imgid'] for i in images]
    tfidf_df.set_index('label',inplace=True)
    print('TF-IDF Score:',baseline_model(text_tags, images, 2, lambda x,y: tfidf_score(tfidf_df,x,y)))

    # evaluation
