import time
import json
import numpy as np
import pandas as pd
from src import constants
import tensorflow as tf
import tensorflow_hub as hub

#csv paths
image_summary_path = f'{constants.CLEAN_DIR}/{constants.Media_Prefix}summary.csv'
data_directory = constants.DATA_DIR
#read as df
df_image = pd.read_csv(image_summary_path)

#load pretrained sentence embeddings
print(f'Loading pretrained USE... \n')
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

#save filename
img_idx_filename = constants.img_idx_filename
#load index dictionaries
with open(f'{constants.DATA_DIR}/{img_idx_filename}', 'r') as img_idx_file:
     img_idx_dict = json.load(img_idx_file)

print(f'{len(df_image)} images found')
print(f'Working on image headlines... \n')
i = 0 #track progress
img_USE_embedding = np.zeros((len(img_idx_dict)-500, 512))
print(f'USE embedding matrix initiated with shape: {img_USE_embedding.shape} \n')
start_time = time.time()
for idx in df_image.id.values:
    headline = df_image[df_image.id == idx].headline.values[0]
    i += 1
    if i % 500 == 0:
        print(f'Working on image #{i}')
        print(f'Time spent: {time.time() - start_time}s \n')
        start_time = time.time()
    #get sentence embeddings
    sentence_embeddings = embed([headline])
    #get image id
    img_idx = img_idx_dict[idx]
    try:
        img_USE_embedding[img_idx] = sentence_embeddings
    except:
        print(headline)

#save compressed matrix
print(f'Saving compressed matrix... \n')
np.savez_compressed(f'{constants.DATA_DIR}/{constants.img_USE_embedding_matrix_filename}', img_USE_embedding)
print('Complete!')
