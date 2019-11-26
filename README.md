ac297r-capstone-project
==============================

### Creating a dev environment

Create a new Python virtualenv with 3.6.8+. Run `pip install -r requirements.txt`.

To run the tests, run `pytest test_project.py` from the project root.

### Data cleaning and preprocessing pipeline

Below is the data cleaning / preprocessing stream now to get cleaned training, test, and validation dataset:

- run `duplicate_images.py` in `src/data_cleaning/`
- run `clean_data.py` in `src/data_cleaning/`
- run `train_test_split.py` in `src/preprocessing/`

### Running the application

You can `make api` to run locally. The app will be available at [http://localhost:8000](http://localhost:8000).

For now, you might have to copy the `thumbnail` directory into `src > ui > static > img`.

### Project Organization

    ├── Makefile
    ├── README.md
    ├── models
    ├── notebooks
    ├── references
    ├── requirements.txt
    ├── setup.py
    ├── src
    │   ├── __init__.py
    │   └── build_features.py
    ├── submissions
    │   ├── final-presentation
    │   ├── lighting-talk-1
    │   ├── lighting-talk-2
    │   ├── midterm
    │   ├── milestone-1
    │   ├── milestone-2
    │   └── partners-reports
    └── test_project.py

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
