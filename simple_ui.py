"""
Class Description
"""

from emotions_engine import EngineObserver

class SentimeterSimpleUI(EngineObserver):
    def __init__(self) -> None:
        super().__init__("SimpleUI")
        
    def update(self,message,emotions):
        print(emotions)
        print(message)
        
