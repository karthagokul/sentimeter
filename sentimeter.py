from intelli_speech import IntelliSpeech
import emotions_engine
from emotions_engine import EmotionsEngine
from threading import Thread
from time import sleep


class Sentimeter:
    listener = IntelliSpeech()
    display_timer = None
    active = False

    def __init__(self) -> None:
        emotions_engine.engine.run()

    def process_text(self, text_data):
        pass

    def process_text_file(self, file_name):
        pass

    def print(self):
        while self.active:
            emotions_engine.eqbank.print()
            sleep(5)

    def start_listening(self):
        if self.active:
            print("Another Listening is Ongoing")
            return
        self.active = True
        # self.display_timer = Thread(target=self.print).start()
        self.listener.listen()

    def stop(self):
        emotions_engine.engine.stop()
        if self.active:
            self.active = False
            self.listener.stop()
