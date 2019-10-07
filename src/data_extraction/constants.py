import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parents[2].resolve()
DATA_DIR = PROJECT_ROOT / "data"
ARTICLE_DIR = PROJECT_ROOT / "data" / "article"
IMAGE_DIR = PROJECT_ROOT / "data" / "image"
THUMBNAIL_DIR = PROJECT_ROOT / "data" / "thumbnail"
FULL_TEXT_DIR = PROJECT_ROOT / "data" / "full_text"
