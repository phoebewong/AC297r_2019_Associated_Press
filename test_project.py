from pathlib import Path

def test_data_dir_exists():
    dir = Path(__file__).parents[0].resolve()
    data_dir = Path('{}/data'.format(dir))
    assert data_dir.is_dir()

def test_csv_outputs():
    dir = Path(__file__).parents[0].resolve()
    csv_dir = Path('{}/data/csv_outputs'.format(dir))
    assert csv_dir.is_dir()
