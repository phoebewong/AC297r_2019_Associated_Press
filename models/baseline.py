# baseline model

### FUNCTIONS ###

# similarity metrics
def baseline_score(text, img):
	return len(set(text) & set(img['tags']))

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
	print(baseline_model(text_tags, images, 2, baseline_score))