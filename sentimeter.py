from intelli_speech import IntelliSpeech
import emotions_engine
from emotions_engine import EmotionsEngine
from threading import Thread
from time import sleep
from sentimeter_ui import SentimeterUI

class Sentimeter:
    listener = IntelliSpeech()
    active = False
    
    def __init__(self) -> None:
        pass

    def setup_ui(self):
        # Add a protection mechanism to avoid recreation
        ui = SentimeterUI()
        emotions_engine.engine.bank.register(ui)

    def process_text(self, text_data):
        self.setup_ui()
        pass

    def process_text_file(self, file_name):
        self.setup_ui()
        pass

    def process_audio_file(self,file_name):
        self.setup_ui()
        self.listener.process_audio_file(file_name)

    def start_listening(self):
        if self.active:
            print("Another Listening is Ongoing")
            return 
        self.setup_ui()
        self.listener.listen()        
        

    def stop(self):
        print("Stopping Sentimeter")
        if self.active:
            self.active = False
            self.listener.stop()
