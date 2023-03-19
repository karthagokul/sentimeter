#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
IntelliAudio Class who proces live speech Audio Data file , Todo : May be split the class?
"""

import logging
from threading import Thread
from queue import Queue
import speech_recognition as sr
import core.emotions_engine as emotions_engine
from core.emotions_engine import SentiMeterModule
from core.sttengine import STTEngine
from core.user_interfaces import SentimeterSimpleUI


class STTLiveTranscoder(Thread):
    """
    Threaded implementation to handle live audio with a processing FIFO
    """

    def __init__(self, backend):
        """
        Constructor
        """
        Thread.__init__(self)
        self.backend = backend
        self.queue = Queue()
        self.user_interface = SentimeterSimpleUI("Live UI")

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
            emotions_engine.engine.process_text(result)
        return True


class LiveSpeechModule(SentiMeterModule):
    """
    Classs Abstracts Audio Related features
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.entries = []
        self.backend = STTEngine(self.recognizer)
        self.sttrunner = STTLiveTranscoder(self.backend)

    def start(self):
        """
        Process Microphone
        """
        super().start()
        self.sttrunner.start()
        while True:
            with sr.Microphone() as source:
                # read the audio data from the default microphone
                audio_data = self.recognizer.record(source, duration=5)
                self.sttrunner.put_data(audio_data)

    def stop(self):
        """
        Routines to stop the Engine
        """
        super().stop()
        logging.debug("Stopping IntelliAudio")
        if not self.sttrunner.is_alive:
            self.sttrunner.join(1)
