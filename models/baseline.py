# baseline model
import nltk
nltk.download('wordnet')
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