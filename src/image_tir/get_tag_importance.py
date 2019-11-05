import json
import time
import numpy as np
import pandas as pd
from src import constants
from measure_tags import MeasureTag
from collections import defaultdict

#get image ids
data_dir = constants.CLEAN_DIR
image_prefix = constants.Media_Prefix
data = pd.read_csv(f'{data_dir}/{image_prefix}summary.csv')
#starting idx to continue tag importance measurement
start_idx = 0
img_ids = data.id.values[start_idx:]
output_dir = constants.DATA_DIR
output_ot_filename = constants.img_ot_filename
output_st_filename = constants.img_st_filename
print(f'Total number of image to process: {len(img_ids)} \n')

#tag types
st_types = ['org', 'place', 'subject']
ot_types = ['person']

#cache dictionaries for image tag importances
ot_history = defaultdict(dict)
st_history = defaultdict(dict)

track_progress = start_idx
track_list = np.arange(1, int(len(img_ids)), 1000)
start_time = time.time()

for idx in img_ids:
    track_progress += 1
    if track_progress % 100 == 0:
        print(f'Processing time: {time.time() - start_time}')
        print(f'Working on image #{track_progress}\n')
    try:
        image = MeasureTag(idx, st_types, ot_types)
        image.get_descriptions() #get image descriptions
        image.get_st_importance() #get scene tag importance
        image.get_ot_importance() #get object tag importance
        ot_history[idx] = image.ot_importance
        st_history[idx] = image.st_importance
        print(image.st_importance)
        print(image.ot_importance)
        print(time.time()-start_time)
        if track_progress in track_list[1:]:
            ot_history_save = dict(ot_history)
            st_history_save = dict(st_history)
            print('Saving history to data directory \n')
            with open(f'{output_dir}/{output_ot_filename}_{track_progress}.json', 'w') as file_1, \
                 open(f'{output_dir}/{output_st_filename}_{track_progress}.json', 'w') as file_2:
                 json.dump(ot_history_save, file_1)
                 json.dump(st_history_save, file_2)
            print(f'#{track_progress} measurement complete \n')
    except:
        print(f'Error occurred at image #{track_progress}')
        break

ot_history = dict(ot_history)
st_history = dict(st_history)

print('Saving final file to data directory')
print(f'#{track_progress} images processed')
with open(f'{output_dir}/{output_ot_filename}_all.json', 'w') as file_1, \
     open(f'{output_dir}/{output_st_filename}_all.json', 'w') as file_2:
     json.dump(ot_history, file_1)
     json.dump(st_history, file_2)
