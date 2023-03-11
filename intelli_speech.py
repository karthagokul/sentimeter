import speech_recognition as sr 
import os 
from threading import Thread
from emotion_engine import EmotionChecker
import sentiqueue

class IntelliSpeech:
    entries=[]
    lang = 'en-IN'
    threads=[]
    recognizer = sr.Recognizer()
    emotion_engine = EmotionChecker()
    def __init__(self) -> None:
        pass

    def speech_to_text(self,audio_data):
        try:
            actual_result = self.recognizer.recognize_google(audio_data, language=self.lang,show_all=True)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        if len(actual_result) == 0:
            return False
        #Lets get the best text
        if "confidence" in actual_result["alternative"]:
            # return alternative with highest confidence score
            best_hypothesis = max(actual_result["alternative"], key=lambda alternative: alternative["confidence"])
        else:
            # when there is no confidence available, we arbitrarily choose the first hypothesis.
            best_hypothesis = actual_result["alternative"][0]
        result=best_hypothesis["transcript"]
        emotion_results=self.emotion_engine.process(result)
        self.entries.append(result)
        sentiqueue.add_text(result)
        #print(self.entries)
        #print(result)
        #print(emotion_results)
        sentiqueue.queue_emotions(emotion_results)
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
    