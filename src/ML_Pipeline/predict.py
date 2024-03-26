import tensorflow as tf
from PIL import Image
import cv2
import numpy as np
import uuid
import os

from .admin import model_path, label_path
from .utility import load_image_into_numpy_array, calculate_area, delete_and_create_folder, shortest_longest_area

import sys
sys.path.append("../models/research")
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# define a class brand object that will take the video input, make predictions and calculate the KPI metrics
class BrandObjectService:
    def __init__(self, video_path):
        self.video_path = video_path
        self.save_path = "./save_path"
        self.predicted_path = './predicted_frames'

        delete_and_create_folder(self.save_path)
        delete_and_create_folder(self.predicted_path)

    def predict(self):
        NUM_CLASSES = 7
        KPIs_dict = dict()


         #Load a (frozen) Tensorflow model into memory.
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(model_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')


        # Loading label map
        label_map = label_map_util.load_labelmap(label_path)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)


        # Size, in inches, of the output images.
        IMAGE_SIZE = (500, 500)
        count = 0
        frame_number = 0

        cap = cv2.VideoCapture(self.video_path)
        with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:
                while cap.isOpened():
                    frame_number += 1

                    ret, frame = cap.read()

                    filename = str(uuid.uuid4()) + ".jpg"
                    fullpath = os.path.join(self.save_path, filename)
                    cv2.imwrite(fullpath, frame)
                    count += 1

                    ### for testing script...
                    if count == 50:
                        break

                    image = Image.open(fullpath)
                    image_np = load_image_into_numpy_array(image)
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})

                    # Visualization of the results of a detection
                    image, box_to_display_str_map = vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8)

                    image_pil = Image.fromarray(np.uint8(image_np)).convert('RGB')
                    im_width, im_height = image_pil.size
                    area_whole = im_width * im_height
                    for key, value in box_to_display_str_map.items():
                        ymin, xmin, ymax, xmax = key
                        (left, right, top, bottom) = (
                            xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
                        area = calculate_area(top, left, bottom, right)

                        percent_area = round(area / area_whole, 2)
                        rindex = value[0].rfind(':')
                        brand_name = value[0][:rindex]

                        if brand_name in KPIs_dict.keys():

                            KPIs_dict[brand_name]['count'] += 1
                            KPIs_dict[brand_name]['area'].append(percent_area)
                            KPIs_dict[brand_name]['frames'].append(frame_number)
                        else:
                            KPIs_dict[brand_name] = {"count": 1}
                            KPIs_dict[brand_name].update({"area": [percent_area]})
                            KPIs_dict[brand_name].update({"frames": [frame_number]})

                    full_predicted_path = os.path.join(self.predicted_path, str(uuid.uuid4()) + ".jpg")
                    cv2.imwrite(full_predicted_path, image)
        KPIs_dict = self.process_kpi(KPIs_dict)
        return KPIs_dict


     # define a function that will return the dictonary with KPI metrics per logo
    def process_kpi(self, KPIs_dict):
        for each_brand, analytics_dict in KPIs_dict.items():
            area = analytics_dict['area']
            response = shortest_longest_area(area)
            KPIs_dict[each_brand].update(response)
        return KPIs_dict
