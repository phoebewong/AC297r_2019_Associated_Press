import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parents[2].resolve()
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_CSV_DIR = PROJECT_ROOT / "data" / 'csv_outputs'

ARTICLE_DIR_NAME = 'article'
IMAGE_DIR_NAME = 'image'
FULL_TEXT_DIR_NAME = 'full_text'
DATA_TRUTH = 'HarvardCapstone.txt'
