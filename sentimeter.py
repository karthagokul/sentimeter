import logging
from intelli_audio import IntelliAudio
from time import sleep
from user_interfaces import SentimeterSimpleUI
#from user_interfaces import SentimeterUI

class Sentimeter:
    '''
    The Application class
    '''
    listener = IntelliAudio()
    
    def __init__(self) -> None:
        '''Constructor'''
        pass

    def process_text(self, text_data):
        '''
        Process Given Text data
        '''
        pass

    def process_text_file(self, file_name):
        '''
        Process a Text file
        '''
        #ui=SentimeterUI()
        pass

    def process_audio_file(self,file_name):
        '''
        Process Audio File
        '''
        ui=SentimeterSimpleUI("AudioProcessingUI")
        self.listener.process_audio_file(file_name)

    def start_listening(self):
        '''
        Process Live Speech from Microphone
        '''
        #ui=SentimeterUI()
        self.listener.listen()
        return
        
    def stop(self):
        '''
        Stops Engine
        '''
        self.listener.stop()
        return