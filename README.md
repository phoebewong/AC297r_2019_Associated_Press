## AC297r Capstone Project: A Text-to-Image Recommendation System for the Associated Press
Karina Huang, Dianne Lee, Abhimanyu Vasishth, Phoebe Wong.
TF: Isaac Slavitt

### About the Project

We create a Text-to-Image Recommendation system that takes the text and headline of an article and recommends a set of best matching photos from AP’s archive.

![UI](readme_images/ui.png)

### Deliverables

View our [Poster](https://github.com/phoebewong/AC297r_2019_Associated_Press/blob/master/submissions/final-presentation/ap_capstone_final_poster.pdf) and our [Final Presentation](https://github.com/phoebewong/AC297r_2019_Associated_Press/blob/master/submissions/final-presentation/ap_capstone_final_presentation.pdf) in the `submissions` folder. In addition, we also wrote a blog on Towards Data Science that you can read [here](todo).

--------

### How to Install and Run the Project

#### If you don't have Python 3.6.9

1. `brew install pyenv`
2. `pyenv install 3.6.9`
3. `pyenv local 3.6.9`
4. `PATH="~/.pyenv/versions/3.6.9/bin:${PATH}"`

#### Create a virtual environment (Python 3.6.9)

1. `python3 -m venv capstone-test`
2. `source capstone-test/bin/activate`
3. `python --version` should be 3.6.9
4. `pip install --upgrade pip` optionally
5. `pip list` lists the following:

```
pip version 19.3.1
setuptools version 40.6.2
```

#### Clone our Github repository

1. `git clone https://github.com/phoebewong/AC297r_2019_Associated_Press.git`
2. `cd AC297r_2019_Associated_Press/`

#### Installing libraries

1. `pip3 install -r requirements.txt`
2. `pip list` will now list all our requirements
3. `python -m spacy download en` to install the spacy model

#### Sensitive files

There are two sensitive files: one is our API key for the taxonomy data and the second is the API key for getting data from our on-demand queue given to us by the AP. These are the instructions for the the first file

1. Place the `tagging_api_password.ini` file in `src`
2. Rename the above file `password.ini`
3. Copy the above file to `src/taxonomy_data` and keep the name of the file the same (both files should be called `password.ini`

These are the instructions for the second set of files

1. Place the `on_demand_password.ini` file in `src/data_extraction` and rename the file `password.ini`

If you are using your own files, make sure you call them `password.ini` and place them in the appropriate directories. The format of the file is as follows:

```
[key]
apikey = yourApiKeyHere
```
#### Getting the data

1. Download the data (about 15gb) from google drive [link](https://drive.google.com/file/d/12vmDT-GueP2-DooyaeQwEFrFz9K7SS_7/view?usp=sharing)
2. Unzip the data within the `src` folder. There should be a `src/data` folder now
3. If there is a folder called `__MACOSX` now created in the root directory of the github repository alongside the `data` directory, this folder can be deleted using `rm -rf __MACOSX`.
4. Copy the folder `src/data/preview` and `src/data/thumbnail` into `src/ui/static/img`
5. A sanity check: `ls src/ui/static/img` should show the folders `thumbnail`, `preview` and `spinner.gif`

#### Running the app

Run `make api` and go to: `http://127.0.0.1:8000/` to test it out

#### Testing

Run `pytest test_project.py` from the project root.

--------

### Project Organization

#### Data

TODO

#### Src

TODO

--------

#### Acknowledgements

We would like to acknowledge our mentors Pavlos Protopapas and Isaac Slavitt at Harvard for their guidance throughout the semester. We would also like to thank Veronika Zielinska and David Fox from the Associated Press for their support.

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
