from ML_Pipeline.predict import BrandObjectService


'''Prediction on given test video '''
video_path = "../input/test_video.mp4"

## call the class object 
brand_expo_obj = BrandObjectService(video_path)

## make predictions
kpi_s = brand_expo_obj.predict()

## print the dictonary with KPI metrics as outpur per logo
print(kpi_s)

