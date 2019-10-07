import constants

data_directory = constants.DATA_DIR
data_truth = constants.DATA_TRUTH
data_truth_path = f'{data_directory}/{data_truth}'

def intended_data(idx, article_idx, data_truth_path = data_truth_path):
    with open(data_truth_path, 'r') as file_truth:
        if idx or article_idx in file_truth.read():
            file_truth.close()
            return True
        else:
            file_truth.close()
            return False
