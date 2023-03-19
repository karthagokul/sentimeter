#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for processing offline Audiofile
"""
import core.emotions_engine as emotions_engine
from core.emotions_engine import SentiMeterModule
from pydub import AudioSegment
from pydub.silence import split_on_silence
from core.sttengine import STTEngine
import os
import logging
import speech_recognition as sr
from core.user_interfaces import SentimeterSimpleUI


class AudioModule(SentiMeterModule):
    """
    Classs Abstracts Audio Related features
    """

    def __init__(self, path) -> None:
        """
        Constructor
        path : location to a .wav file , in future we can add support for mp3 etc
        """
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.backend = STTEngine(self.recognizer)
        self.path = path
        self.ui = SentimeterSimpleUI("Audio UI")

    def start(self):
        super().start()
        transcription = ""
        logging.info("Processing Audio File " + self.path)
        # open the audio file using pydub
        sound = AudioSegment.from_wav(self.path)
        # split audio sound where silence is 1000 miliseconds or more and get chunks
        chunks = split_on_silence(
            sound,
            # experiment with this value for your target audio file
            min_silence_len=1000,
            # adjust this per requirement
            silence_thresh=sound.dBFS - 14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=1000,
        )
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        # process each chunk
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_data = self.recognizer.record(source)
                transcription += " " + self.backend.speech_to_text(audio_data)
        emotions_engine.engine.process_text(transcription)
        return True

    def stop(self):
        """
        Routines to stop the Engine
        """
        super().stop()
        logging.debug("Stopping IntelliAudio")
        if not self.sttrunner.is_alive:
            self.sttrunner.join(1)

        return True
