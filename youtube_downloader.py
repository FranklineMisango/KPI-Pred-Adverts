from pytube import YouTube 
  
# where to save 
SAVE_PATH = "data" 
  
# link of the video to be downloaded 
link="https://youtu.be/CrnraEVaWTM?si=98j9FcMFYdPFhmBr"
  
try: 
    yt = YouTube(link) 
except: 
    print("Connection Error") #to handle exception 
  
yt.streams.first().download()

print('Task Completed!') 
