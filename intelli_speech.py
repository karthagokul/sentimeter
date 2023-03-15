import speech_recognition as sr
import os
from threading import Thread
import emotions_engine
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

class IntelliSpeech:
    
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.entries = []
        self.lang = "en-IN"
        self.threads = []

    def speech_to_text(self, audio_data):
        try:
            actual_result = self.recognizer.recognize_google(
                audio_data, language=self.lang, show_all=True
            )
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Error service; {0}".format(e))
        if len(actual_result) == 0:
            return False

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
        emotions_engine.engine.process_text(result)
        return True

    def process_audio_file(self,path):
        # open the audio file using pydub
        sound = AudioSegment.from_wav(path)  
        # split audio sound where silence is 700 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            # experiment with this value for your target audio file
            min_silence_len = 500,
            # adjust this per requirement
            silence_thresh = sound.dBFS-14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=500,
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
                audio_listened = self.recognizer.record(source)
                self.speech_to_text(audio_listened)

        return True

    def listen(self):
        while True:
            with sr.Microphone() as source:
                # read the audio data from the default microphone
                audio_data = self.recognizer.record(source, duration=5)
                process = Thread(target=self.speech_to_text, args=[audio_data])
                process.start()
                self.threads.append(process)

    def __del__(self):
        self.stop()

    def stop(self):
        for process in self.threads:
            process.join()
