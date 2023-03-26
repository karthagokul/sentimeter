import logging
import os
import logging
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr

from pysentimeter.sources import BaseSource
from pysentimeter.speech_to_text import STTEngine

import json


class AudioSource(BaseSource):
    def __init__(self, engine, path) -> None:
        super().__init__(engine)
        self.recognizer = sr.Recognizer()
        self.backend = STTEngine(self.recognizer)
        self.path = path

    def run(self):
        transcription = ""
        logging.info("Processing Audio File %s", self.path)
        logging.info(
            "Depending on the Size of Audio , The process takes some time, Have a coffee !"
        )
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
        folder_name = ".audio-chunks"
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
                logging.debug("Processed Audio Chunk %s" % chunk_filename)
        logging.info("Finished Processing")
        self.engine.process(transcription)
        return True

    def on_event(self, results):
        logging.info("Results in JSON follows")
        logging.info(json.dumps(results))
        pass
