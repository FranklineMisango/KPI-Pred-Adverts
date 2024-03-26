from pytube import YouTube 
  
# where to save 
SAVE_PATH = "./" 
  
# link of the video to be downloaded 
link="https://www.youtube.com/watch?v=xWOoBJUqlbI"
  
try: 
    yt = YouTube(link) 
except: 
    print("Connection Error") #to handle exception 
  
yt.streams.first().download()

print('Task Completed!') 
