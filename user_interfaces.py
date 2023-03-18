import emotions_engine
from emotions_engine import EngineObserver

class SentimeterSimpleUI(EngineObserver):
    def __init__(self, name) -> None:
        super().__init__(name)
        emotions_engine.engine.add_observer(self)

    def on_event(self,message,emotions):
        print("Transcription")
        print(message)
        print("Emotions")
        print(emotions)
