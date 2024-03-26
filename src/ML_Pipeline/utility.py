import numpy as np
import os
import shutil

# function to load images into a numpy array
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

# function to calculate the area of logo displayed
def calculate_area(x1, y1, x2, y2):
    xDiff = abs(x1 - x2)
    yDiff = abs(y1 - y2)
    area = xDiff * yDiff
    return area

# function to calculate the shortest and largest area of logo displayed
def shortest_longest_area(area_list):
    area_list.sort()
    shortest = area_list[0]
    longest = area_list[-1]
    response = {
        "shortest": shortest,
        "longest": longest
    }
    return response

# function to delete and create a folder
def delete_and_create_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path, 0o755)
    else:
        os.makedirs(folder_path, 0o755)
