import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parents[1].resolve()
DATA_DIR = PROJECT_ROOT / 'data'

# directories
ARTICLE_DIR = PROJECT_ROOT / 'data' / 'article'
IMAGE_DIR = PROJECT_ROOT / 'data' / 'image'
THUMBNAIL_DIR = PROJECT_ROOT / 'data' / 'thumbnail'
EMBEDDING_DIR = PROJECT_ROOT / 'data' / 'embeddings'
PREVIEW_DIR = PROJECT_ROOT / 'data' / 'preview'
FULL_TEXT_DIR = PROJECT_ROOT / 'data' / 'full_text'
OUTPUT_CSV_DIR = PROJECT_ROOT / 'data' / 'csv_outputs'
TAXONOMY_DIR = PROJECT_ROOT / 'data' / 'taxonomy_data'
CLEAN_DIR = PROJECT_ROOT / 'data' / 'clean_data'
HIST_DIR = PROJECT_ROOT / 'data' / 'clean_data' / 'clean_history'
TRAIN_TEST_DIR = PROJECT_ROOT / 'data' / 'train_test_data'
TRAIN_DIR = PROJECT_ROOT / 'data' / 'train_test_data'/'train'
TEST_DIR = PROJECT_ROOT / 'data' / 'train_test_data'/'test'
VAL_DIR = PROJECT_ROOT / 'data' / 'train_test_data'/'val'
LOGGING_DIR = PROJECT_ROOT / 'data' / 'logged_data'
STANFORD_PARSER = PROJECT_ROOT / 'stanford-parser-full-2018-10-17'
SRC_DIR = PROJECT_ROOT / 'src'
PREPROCESSING_DIR = PROJECT_ROOT / 'src' / 'preprocessing'
USE_MODEL_DIR = PROJECT_ROOT / 'data' / 'use_model_4'

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
tag_idx_filename = 'tag_idx.json'
img_idx_filename = 'img_idx.json'
obj_imp_filename = 'object_tag_importance_all.json'
scn_imp_filename = 'scene_tag_importance_all.json'
img_bert_embedding_filename = 'img_headline_bert_embeddings.json'

#npz file name
imp_matrix_filename = 'imp_matrix.npz'
ind_matrix_filename = 'ind_matrix.npz'
normalized_imp_matrix_filename = 'normalized_imp_matrix.npz'
normalized_img_bert_matrix_filename = 'img_headline_bert_embedding_matrix.npz'
img_USE_embedding_matrix_filename = 'img_USE_embedding.npz'
