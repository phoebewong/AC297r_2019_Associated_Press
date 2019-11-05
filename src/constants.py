import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parents[1].resolve()
DATA_DIR = PROJECT_ROOT / 'data'

# directories
ARTICLE_DIR = PROJECT_ROOT / 'data' / 'article'
IMAGE_DIR = PROJECT_ROOT / 'data' / 'image'
THUMBNAIL_DIR = PROJECT_ROOT / 'data' / 'thumbnail'
FULL_TEXT_DIR = PROJECT_ROOT / 'data' / 'full_text'
OUTPUT_CSV_DIR = PROJECT_ROOT / 'data' / 'csv_outputs'
TAXONOMY_DIR = PROJECT_ROOT / 'data' / 'taxonomy_data'
CLEAN_DIR = PROJECT_ROOT / 'data' / 'clean_data'
HIST_DIR = PROJECT_ROOT / 'data' / 'clean_data' / 'clean_history'
TRAIN_TEST_DIR = PROJECT_ROOT / 'data' / 'train_test_data'
TRAIN_DIR = PROJECT_ROOT / 'data' / 'train_test_data'/'train'
TEST_DIR = PROJECT_ROOT / 'data' / 'train_test_data'/'test'
VAL_DIR = PROJECT_ROOT / 'data' / 'train_test_data'/'val'
STANFORD_PARSER = PROJECT_ROOT / 'stanford-parser-full-2018-10-17'
PREPROCESSING_DIR = PROJECT_ROOT / 'src' / 'preprocessing'

#train test split params
data_split_random_state = 8
test_size = 0.2
val_size = 0.1

# folder names
ARTICLE_DIR_NAME = 'article'
IMAGE_DIR_NAME = 'image'
FULL_TEXT_DIR_NAME = 'full_text'

# original csv file prefix
Text_Prefix = 'article_'
Media_Prefix = 'image_'

# txt files
DATA_TRUTH = 'HarvardCapstone.txt'
IMAGE_DUPLICATES_FILENAME = DATA_DIR / 'image_duplicates.txt'
media_removal_hist_name = 'removed_media.txt'
article_removal_hist_name = 'removed_article.txt'
train_aid_filename = 'train_aid.txt'
test_aid_filename = 'test_aid.txt'
val_aid_filename = 'val_aid.txt'

#pickle files
word2idx_filename = 'word2idx.pkl'
idx2word_filename = 'idx2word.pkl'

#json files prefix
img_ot_filename = 'object_tag_importance'
img_st_filename = 'scene_tag_importance'
