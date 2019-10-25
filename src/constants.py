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

# folder names
ARTICLE_DIR_NAME = 'article'
IMAGE_DIR_NAME = 'image'
FULL_TEXT_DIR_NAME = 'full_text'

# original csv file prefix
Text_Prefix = 'article_'
Media_Prefix = 'image_'

# removal history file name
media_removal_hist_name = 'removed_media.txt'
article_removal_hist_name = 'removed_article.txt'

# txt files
DATA_TRUTH = 'HarvardCapstone.txt'
IMAGE_DUPLICATES_FILENAME = DATA_DIR / 'image_duplicates.txt'
