from intelli_speech import IntelliSpeech
import sentiqueue
import random
import time

from threading import Thread
from time import sleep
import re, sys

class Sentimeter:
    listener =IntelliSpeech()
    display_timer=None
    active=True
    def __init__(self) -> None:
        pass
    
    def print(self):
        while self.active:
            print(sentiqueue.text_buffer)
            print(sentiqueue.emotions_average)
            sleep(5)

    def start(self):
        self.active=True
        self.display_timer=Thread(target=self.print).start()
        self.listener.listen()

    def stop(self):
        self.active=False
        self.listener.stop()
        pass
