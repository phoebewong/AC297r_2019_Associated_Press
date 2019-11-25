from sklearn.linear_model import LinearRegression
from sklearn.compose import TransformedTargetRegressor

import pandas as pd
import numpy as np
from src import constants

if __name__ == '__main__':
    csv_file = constants.OUTPUT_CSV_DIR / 'image_person.csv'
    data = pd.read_csv(csv_file)

    # very basic model
    X = np.random.randint(low=0, high=len(data), size=len(data))
    data['X'] = X
    data['Y'] = X

    model = LinearRegression().fit(data[['X']], data[['Y']])
