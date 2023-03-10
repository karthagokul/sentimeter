import speech_recognition as sr 
import os 
from threading import Thread

class LiveSpeech:
    entries=[]
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.lang = 'en-IN'
        self.threads = []

    def speech_to_text(self,audio_data):
        try:
            actual_result = self.recognizer.recognize_google(audio_data, language=self.lang,show_all=True)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        #Lets get the best text
        if "confidence" in actual_result["alternative"]:
            # return alternative with highest confidence score
            best_hypothesis = max(actual_result["alternative"], key=lambda alternative: alternative["confidence"])
        else:
            # when there is no confidence available, we arbitrarily choose the first hypothesis.
            best_hypothesis = actual_result["alternative"][0]
        self.entries.append(best_hypothesis["transcript"])
        print(self.entries)
        return True

    def listen(self):
        while True:
            with sr.Microphone() as source:
                # read the audio data from the default microphone
                print("listening")
                audio_data = self.recognizer.record(source, duration=5)
                process = Thread(target=self.speech_to_text, args=[audio_data])
                process.start()
                self.threads.append(process)

    def __del__(self):
        for process in self.threads:
            process.join()