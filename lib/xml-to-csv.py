import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

# source and credits:
# https://raw.githubusercontent.com/datitran/raccoon_dataset/master/xml_to_csv.py

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def train():
    annotation_path = os.path.join('/home/poonam/artivatic/freeTime/BrandExposure/data/train', 'annotation')
    xml_df = xml_to_csv(annotation_path)
    
    labels_path = os.path.join('/home/poonam/artivatic/freeTime/BrandExposure/data','train.csv')
    xml_df.to_csv(labels_path, index=None)


train()

