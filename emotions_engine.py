import logging
import queue
import threading
import sys
import text2emotion as te
from time import sleep

class EngineObserver:
    def __init__(self, name):
        logging.debug("New Subscriber is getting created " + name)
        self.name = name
    def update(self, message,emotions):
        pass

class EnginePublisher:
    subscribers=[]
    def __init__(self):
        pass

    def register(self, who):
        logging.debug("Registering Observer ")
        self.subscribers.append(who)
    def unregister(self, who):
        self.subscribers.remove(who)

    def dispatch(self, text,emotions):
        for subscriber in self.subscribers:
            subscriber.update(text,emotions)


class EmotionsBank (EnginePublisher):
    emotions_counter = 0
    emotions_average = {}
    emotions_average["Happy"] = 0
    emotions_average["Angry"] = 0
    emotions_average["Surprise"] = 0
    emotions_average["Sad"] = 0
    emotions_average["Fear"] = 0
    text_buffer = ""
    
    def __init__(self) -> None:
        self.threadLock = threading.Lock()
        pass

    def deposit(self, text, entry):
        with self.threadLock:
            self.emotions_counter += 1
            self.text_buffer +=" " +text 
            self.emotions_average["Happy"] = (
                self.emotions_average["Happy"] + entry["Happy"]
            )
            self.emotions_average["Angry"] = (
                self.emotions_average["Angry"] + entry["Angry"]
            )
            self.emotions_average["Surprise"] = (
                self.emotions_average["Surprise"] + entry["Surprise"]
            )
            self.emotions_average["Sad"] = self.emotions_average["Sad"] + entry["Sad"]
            self.emotions_average["Fear"] = (
                self.emotions_average["Fear"] + entry["Fear"]
            )
            self.dispatch(self.text_buffer,self.emotions_average)
            logging.debug("Adding Text to Bank" + text)

class EmotionsEngine():
    def __init__(self) -> None:
        self.bank = EmotionsBank()       

    def process_text(self, result):
        emotion_results = te.get_emotion(result)
        self.bank.deposit(result, emotion_results)

# global data instance
engine = EmotionsEngine()
# global end
