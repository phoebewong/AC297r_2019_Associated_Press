from src import constants
import os
import numpy as np
from PIL import Image
import time

if __name__ == '__main__':

    start_time = time.time()
    path = constants.THUMBNAIL_DIR
    imgs = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    print('Number of files', len(imgs), time.time() - start_time)

    def get_id(path):
        filename = path.split('/')[-1]
        id = filename.split('.')[0]
        return id

    # computing hashes of the image rather than comparing the image itself
    print('Computing Hashes')
    hashes = np.zeros(shape=len(imgs))
    for i, img_file in enumerate(imgs):
        image = np.array(Image.open(img_file))
        hashes[i] = hash(image.tostring())
    print('Hashes Shape', hashes.shape, time.time() - start_time)

    print('Computing Similar Pairs')
    similar_pairs = []

    for i in range(len(hashes)):
        # progress
        if i % 10000 == 0 and i > 0:
            print(i, time.time() - start_time)

        # comparing this hash with all other hashes
        repeat_hashes = np.repeat([hashes[i]], len(hashes), axis=0)
        find_matches = (np.abs(repeat_hashes - hashes) == 0)*1.0
        find_matches[i] = 0 # remove the element itself
        inds = np.where(find_matches > 0)[0]

        # adding the matching indices to the list of lists
        if len(inds) > 0:
            # not duplicating rows
            # i.e. if we have a row [img49, img71, img90]
            # then we do not add another row [img71, img49, img90]
            if np.min(inds) < i:
                continue

            ids = [get_id(imgs[int(ind)]) for ind in inds]
            ids.insert(0, get_id(imgs[i]))
            similar_pairs.append(','.join(ids))

    print('Saving to txt', time.time()-start_time)
    name = str(constants.DATA_DIR) + '/image_duplicates.txt'
    np.savetxt(name, similar_pairs, delimiter=",", fmt='%s')
