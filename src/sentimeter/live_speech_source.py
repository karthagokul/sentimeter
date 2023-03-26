import logging
import json
import speech_recognition as sr
from sentimeter.sources import BaseSource
from sentimeter.speech_to_text import STTEngine
from threading import Thread
from queue import Queue


class STTLiveTranscoder(Thread):
    """
    Threaded implementation to handle live audio with a processing FIFO
    """

    def __init__(self, backend, engine):
        """
        Constructor
        """
        Thread.__init__(self)
        self.backend = backend
        self.engine = engine
        self.queue = Queue()

    def put_data(self, audio_data):
        """
        Adds the audio data to processing queue
        """
        self.queue.put(audio_data)

    def run(self):
        """
        Runner
        """
        while True:
            audiodata = self.queue.get()
            result = self.backend.speech_to_text(audiodata)
            if result != "":
                self.engine.process(result)
            else:
                logging.info("Skipping Silence")
        return True


class LiveSpeechSource(BaseSource):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        self.recognizer = sr.Recognizer()
        self.entries = []
        self.backend = STTEngine(self.recognizer)
        self.sttrunner = STTLiveTranscoder(self.backend, engine)

    def run(self):
        self.sttrunner.start()
        while True:
            with sr.Microphone() as source:
                # read the audio data from the default microphone
                audio_data = self.recognizer.record(source, duration=5)
                self.sttrunner.put_data(audio_data)
        return True

    def on_event(self, results):
        logging.info("Results in JSON follows")
        logging.info(json.dumps(results))
        pass
