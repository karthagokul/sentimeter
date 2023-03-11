from queue import Queue
import threading
threadLock = threading.Lock()
emotions_counter= 0
emotions_average={}
emotions_average["Happy"]=0
emotions_average["Angry"]=0
emotions_average["Surprise"]=0
emotions_average["Sad"]=0
emotions_average["Fear"]=0
text_buffer=""

def add_text(text):
    global threadLock
    global text_buffer
    with threadLock:
        text_buffer+=text

def queue_emotions(entry):
    global threadLock
    global emotions_counter
    with threadLock:
        emotions_counter += 1
        emotions_average["Happy"]=(emotions_average["Happy"]+entry["Happy"]) 
        emotions_average["Angry"]=(emotions_average["Angry"]+entry["Angry"]) 
        emotions_average["Surprise"]=(emotions_average["Surprise"]+entry["Surprise"]) 
        emotions_average["Sad"]=(emotions_average["Sad"]+entry["Sad"]) 
        emotions_average["Fear"]=(emotions_average["Fear"]+entry["Fear"]) 
        print(emotions_average)
        
