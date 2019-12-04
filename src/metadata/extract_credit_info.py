###extract credit information for citation purposes

#dependencies
import os
from src import constants
import json
from process_metadata import Metadata

#directory paths
data_directory = constants.DATA_DIR
image_directory = constants.IMAGE_DIR

if __name__ == '__main__':
    credit_info = dict()
    for file in os.listdir(image_directory):
        if '.json' in file:
            filepath = f'{image_directory}/{file}'
            with open(filepath, 'r') as jsonfile:
                image_info = json.load(jsonfile)
                image_metadata = Metadata(image_info)
            #image id
            id = image_metadata.id
            #photographer_code
            photographer_code = image_metadata.get_photographer_code()
            #creditline info
            creditline = image_metadata.get_creditline()
            #update dictionary
            credit_info.update({id: {'photographer_code': photographer_code, 'creditline': creditline}})
    savefilename = f'{data_directory}/image_creditinfo.json'
    print('Saving to json file')
    with open(savefilename, 'w') as output_file:
        json.dump(credit_info, output_file)
