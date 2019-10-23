import pathlib

#directory path
PROJECT_ROOT = pathlib.Path(__file__).parents[2].resolve()
DATA_DIR = PROJECT_ROOT / "data" / 'csv_outputs'
OUTPUT_DIR = PROJECT_ROOT / "data" / 'clean_data'
HIST_DIR = PROJECT_ROOT / "data" / 'clean_data' / 'clean_history'

#original csv file prefix
Text_Prefix = 'article_'
Media_Prefix = 'image_'

#removal history file name
media_removal_hist_name = 'removed_media.txt'
article_removal_hist_name = 'removed_article.txt'
