# Project Workflow

## Assumption: 
The modular code of the project assumes that we already have a trained object detection model and it does not focus on data collection, labelling and preparation. Although the step by step process has been explained in the video lectures to be replicated by the learners.

## Approach:
1. **Data Collection**: Collect the video of Pepsi brand exposure on YouTube with the youtube_downloader.py script. Video Link - https://www.youtube.com/watch?v=xWOoBJUqlbI

2. **Data Labelling**: Label each frame of the video with the object detection tool LabelImg to identify the appearance of Pepsi and other brands in the video.

3. **Data Preparation**: Prepare the labelled data for training by splitting it into training and testing sets and converting it into a format (XML to CSV to TFrecords) suitable for training an object detection model.

4. **Setting up Tensorflow for Object Detection**: 
   * Clone the repository 
      ``` git clone https://github.com/tensorflow/models.git```
   * Run ```export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim``` inside /models/research directory.

5. **Download the Base Model**: Download the base model- ssd_resnet_50_fpn_coco from the repository https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md and extract.

6. **Model Training**: Get the training files from the previously cloned Tensorflow repository models/research/object_detection. Copy the train.py file from legacy and paste into the base folder and Train an object detection model on the labelled data as explained in the video lectures.

7. **Model Freezing**: Freeze the ckpt files into a frozen graph file for inference.

8. **KPI Calculation:** Calculate Key Performance Indicators (KPIs) such as the total appearance count, largest area percentage, smallest area percentage, and exposure over time comparison to understand the impact of the video on brand exposure.

By following this project workflow, businesses can effectively calculate the brand exposure of their video campaigns and gain insights into the impact of their marketing efforts.



### **Setting up the Modular Code**
The modular code is specifically for inference purposes and not training.
   * Install requirements.txt using following command
   ```pip install -r requirements.txt```

   * Clone the repository 
      ``` git clone https://github.com/tensorflow/models.git```
   * Run ```export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim``` inside /models/research directory.

   * Run Engine.py for all the KPI's metrics

