# Credit: https://gluon-cv.mxnet.io/build/examples_detection/demo_faster_rcnn.html

import constants
import numpy as np
from matplotlib import pyplot as plt
import gluoncv
from gluoncv import model_zoo, data, utils
import mxnet as mx
from os import listdir

def box_params(orig_shape, coords):
    """
    Returns the ratio of the area of a bounding box and the total image
    Also returns the distance of the center of the box from the center of the image
    """
    orig_y, orig_x, orig_nchannels = orig_shape
    x_left, y_top, x_right, y_bottom = coords

    # portrait image
    if orig_x < orig_y:
        x_right = min(x_right, 600)
    # landscape image
    if orig_y <= orig_x:
        y_bottom = min(y_bottom, 600)

    # calculating the area of the box
    area = (x_right - x_left) * (y_bottom - y_top)
    orig_area = orig_x * orig_y
    area_ratio = area/orig_area

    # calculating the center of the box
    cen_x, cen_y = np.mean([x_left, x_right]), np.mean([y_top, y_bottom])
    dist = np.sqrt((cen_x-orig_x/2.)**2 + (cen_y-orig_y/2.)**2)

    return area_ratio, dist

# loading the faster RCNN model
net = model_zoo.get_model('faster_rcnn_resnet50_v1b_voc', pretrained=True)

# x: NDArray, can be fed into the model directly
# orig_img: can be plotted using matplotlib
# resized image short length is 600px

all_files = listdir(constants.THUMBNAIL_DIR)
rand_num = np.random.randint(0, len(all_files))
img_id = str(all_files[rand_num]).split('.')[0]
# im_fname = constants.THUMBNAIL_DIR / str(all_files[rand_num])
im_fname = 'pope2.png'
x, orig_img = data.transforms.presets.rcnn.load_test(str(im_fname))


# inference and display
box_ids, scores, bboxes = net(x)
ax = utils.viz.plot_bbox(orig_img, bboxes[0], scores[0], box_ids[0], class_names=net.classes)
box_ids, scores, bboxes = box_ids.asnumpy(), scores.asnumpy(), bboxes.asnumpy()

indices = (scores[0] > 0.6).flatten()
person_ind = net.classes.index("person")

num_people = np.sum(box_ids[0][indices].flatten() == person_ind)
plt.title('img id: {}. num people: {}'.format(img_id, num_people))

# calculating area of bounding box and distance from center when there is 1 person in the image
if num_people == 1:
    id = box_ids[0][indices].flatten() == person_ind
    box = bboxes[0][indices][id].flatten()
    area, dist = box_params(orig_img.shape, box)
    plt.xlabel('area ratio = {}, dist = {}'.format(area, dist))

plt.show()
