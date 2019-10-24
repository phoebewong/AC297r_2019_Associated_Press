import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parents[1].resolve()
DATA_DIR = PROJECT_ROOT / 'data'
ARTICLE_DIR = PROJECT_ROOT / 'data' / 'article'
IMAGE_DIR = PROJECT_ROOT / 'data' / 'image'
THUMBNAIL_DIR = PROJECT_ROOT / 'data' / 'thumbnail'
FULL_TEXT_DIR = PROJECT_ROOT / 'data' / 'full_text'
OUTPUT_CSV_DIR = PROJECT_ROOT / 'data' / 'csv_outputs'

ARTICLE_DIR_NAME = 'article'
IMAGE_DIR_NAME = 'image'
DATA_TRUTH = 'HarvardCapstone.txt'
IMAGE_DUPLICATES_FILENAME = DATA_DIR / 'image_duplicates.txt'
