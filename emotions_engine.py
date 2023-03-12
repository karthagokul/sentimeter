import queue
import threading
import sys
import text2emotion as te
from time import sleep


class EmotionsBank:
    emotions_counter = 0
    emotions_average = {}
    emotions_average["Happy"] = 0
    emotions_average["Angry"] = 0
    emotions_average["Surprise"] = 0
    emotions_average["Sad"] = 0
    emotions_average["Fear"] = 0
    text_buffer = ""
    threadLock = threading.Lock()

    def deposit(self, text, entry):
        with self.threadLock:
            self.emotions_counter += 1
            self.text_buffer += "\n" + text
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

    def print(self):
        print(self.text_buffer)
        print(self.emotions_average)


class EmotionsEngine:
    item_queue = queue.Queue()
    active = False

    def stop(self):
        self.active = False

    def run(self):
        self.active = True
        self.worker = threading.Thread(target=self.__process_in_background)
        self.worker.start()

    def process_text(self, result):
        self.item_queue.put(result)

    def __process_in_background(self):
        while self.active:
            print("Processing Emotions")
            sleep(1)
            if self.item_queue.empty():
                continue
            text = self.item_queue.get()
            emotion_results = te.get_emotion(text)
            eqbank.deposit(text, emotion_results)
            eqbank.print()


# global data instance
eqbank = EmotionsBank()
engine = EmotionsEngine()
# global end
