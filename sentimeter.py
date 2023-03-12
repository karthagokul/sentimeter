from intelli_speech import IntelliSpeech
import emotions_engine
from emotions_engine import EmotionsEngine
from threading import Thread
from time import sleep
from sentimeter_ui import SentimeterUI

class Sentimeter:
    listener = IntelliSpeech()
    display_timer = None
    active = False
    ui = SentimeterUI()

    def __init__(self) -> None:
        emotions_engine.engine.run()

    def process_text(self, text_data):
        pass

    def process_text_file(self, file_name):
        pass

    def process_audio_file(self,file_name):
        self.__print_progress()
        self.listener.process_audio_file(file_name)

    def __print_progress(self):
        self.active = True
        self.display_timer = Thread(target=self.print).start()

    def print(self):
        while self.active:
            sleep(5)
            self.ui.update_emotions(emotions_engine.engine.bank.emotions_average)
            self.ui.update_transcript(emotions_engine.engine.bank.text_buffer)

    def start_listening(self):
        if self.active:
            print("Another Listening is Ongoing")
            return 
        self.__print_progress()
        self.listener.listen()        
        


    def stop(self):
        print("Stopping Sentimeter")
        emotions_engine.engine.stop()
        if self.active:
            self.active = False
            self.listener.stop()
