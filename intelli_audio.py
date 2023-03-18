"""
IntelliAudio Class who proces live speech Audio Data file , Todo : May be split the class?
"""

import logging
import speech_recognition as sr
import os
from threading import Thread
from queue import Queue
import emotions_engine
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from time import sleep

class STTEngine:
    '''
    Speech to Text Engine, Currently using Google Service, Options to be added for Sphinix
    '''

    def __init__(self,recognizer) -> None:
        '''
        constructor
        '''
        self.recognizer=recognizer
        self.lang = "en-IN"
        pass
    
    def speech_to_text(self,audiodata):
        '''
        function to get the text for inputed audio data
        '''
        try:
            actual_result = self.recognizer.recognize_google(
                audiodata, language=self.lang, show_all=True
            )
        except sr.UnknownValueError:
            logging.fatal("Google Speech Recognition could not understand audio")
            exit(-1)
        except sr.RequestError as e:
            logging.fatal("Error service; {0}".format(e))
            exit(-1)
        if len(actual_result) == 0:
            logging.debug("Unable to get the Speech to Text,Ignoring")
            return ""

        # Lets get the best text
        if "confidence" in actual_result["alternative"]:
            # return alternative with highest confidence score
            best_hypothesis = max(
                actual_result["alternative"],
                key=lambda alternative: alternative["confidence"],
            )
        else:
            # when there is no confidence available, we arbitrarily choose the first hypothesis.
            best_hypothesis = actual_result["alternative"][0]
        result = best_hypothesis["transcript"]
        return result

class STTLiveTranscoder(Thread):
    '''
    Threaded implementation to handle live audio with a processing FIFO
    '''
    def __init__(self, backend):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.backend=backend
        self.queue=Queue()
        self.text=""

    def put_data(self,audio_data):
        '''
        Adds the audio data to processing queue
        '''
        self.queue.put(audio_data)

    def run(self):
        '''
        Runner
        '''
        while True:
            audiodata = self.queue.get()
            result=self.backend.speech_to_text(audiodata)
            emotions_engine.engine.process_text(result)
        return True

class IntelliAudio:
    '''
    Classs Abstracts Audio Related features
    '''
    def __init__(self) -> None:
        '''
        Constructor
        '''
        self.recognizer = sr.Recognizer()
        self.entries = []
        self.backend=STTEngine(self.recognizer)
        self.sttrunner = STTLiveTranscoder(self.backend)

    def process_audio_file(self,path):
        ''' For now only supports Wav
        '''
        transcription=""
        logging.info("Processing Audio File " + path)
        # open the audio file using pydub
        sound = AudioSegment.from_wav(path)  
        # split audio sound where silence is 1000 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            # experiment with this value for your target audio file
            min_silence_len = 1000,
            # adjust this per requirement
            silence_thresh = sound.dBFS-14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=1000,
        )
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_data = self.recognizer.record(source)  
                transcription+=" " + self.backend.speech_to_text(audio_data)
        emotions_engine.engine.process_text(transcription)
        return True

    def listen(self):
        '''
        Process Microphone
        '''
        self.sttrunner.start()
        while True:
            with sr.Microphone() as source:
                # read the audio data from the default microphone
                audio_data = self.recognizer.record(source, duration=5)
                self.sttrunner.put_data(audio_data)                

    def __del__(self):
        self.stop()

    def stop(self):
        '''
        Routines to stop the Engine
        '''
        logging.debug("Stopping IntelliAudio")
        if not self.sttrunner.is_alive:
            self.sttrunner.join(1)
