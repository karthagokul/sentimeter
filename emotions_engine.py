"""
Class Description
"""

import logging
import text2emotion as te
from time import sleep


class EngineObserver:
    def __init__(self, name) -> None:
        '''
        A Name is given for observer
        '''
        self.name = name

    def on_event(self, result, emotions):
        '''
        Observer Abstract Method
        '''
        pass


class EmotionsEngine():
    '''
    The class responsible to identify the emotions of a given text
    '''

    def __init__(self) -> None:
        '''
        constructor , the object acts as singleton
        '''
        self._listeners = {}

    def add_observer(self, observer):
        '''
        The Engine events are propogated via an observer mechanism, Objects can register via this method
        '''
        self._listeners[observer.name] = observer

    def remove_observer(self, observer):
        '''
        Remove an observer ,Todo : Check if observer is not registered to avoid exceptions
        '''
        self._listeners.pop(observer.name)

    def process_text(self, result):
        '''
        The Functions to start the processing
        '''
        emotions = te.get_emotion(result)
        # Lets inform all the listerners
        for obj in self._listeners:
            self._listeners[obj].on_event(result, emotions)


# global data instance
engine = EmotionsEngine()
# global end
