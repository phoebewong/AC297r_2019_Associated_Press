import numpy as np
from scipy.sparse import save_npz, load_npz, csc_matrix
import sys
sys.path.append('../../')
from src import constants
from sklearn.preprocessing import Normalizer

#directory path
data_directory = constants.DATA_DIR
#update this in constants.py
imp_matrix_filename = 'imp_matrix.npz'
print('loading importance matrix \n')
#load presaved matrix and switch back to dense matrix
img_imp_matrix_sparse = load_npz(f'{data_directory}/{imp_matrix_filename}')
print('converting sparse matrix back to dense \n')
img_imp_matrix = img_imp_matrix_sparse.todense()
print('normalizing matrix \n')
#normalize matrix and save
normalized_imp_matrix = Normalizer().fit_transform(img_imp_matrix)
#save as sparse matrix
sparse_normalized_matrix = csc_matrix(normalized_imp_matrix)
print(f'Saving to {constants.normalized_imp_matrix_filename} ...')
save_npz(f'{data_directory}/{constants.normalized_imp_matrix_filename}', sparse_normalized_matrix)
