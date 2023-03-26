from sentimeter.local_backend import LocalBackend
from sentimeter.engine_observer import EngineObserver

# HAPPY = "Happy"
# SAD = "Sad"
# FEAR = "Fear"
# ANGRY = "Angry"
# SURPRISE = "Surprise"
TEXT = "Text"

import logging


class Sentimeter:
    """Class Responsible for the middleware operations"""

    def __init__(self) -> None:
        """constructor"""
        self.backend = LocalBackend()
        self.__listeners = []
        self._enable_logging(logging.DEBUG)

    def _enable_logging(self, lev):
        """enables logging"""
        logging.basicConfig(level=lev, format="[Sentimeter] [%(levelname)-5.5s]  %(message)s")

    def set_backend(self, backend):
        """API to switch the backend"""
        self.backend = backend
        logging.info("Switched to Backend " + self.backend.backend_name)

    def add_observer(self, listener):
        """capture the emotions by adding yourself as observer"""
        self.__listeners.append(listener)

    def remove_observer(self, listener):
        """remove the observer"""
        self.__listeners.remove(listener)

    def process(self, text):
        """The runner"""
        result = {}
        result = self.backend.process(text)
        result[TEXT] = text
        for obj in self.__listeners:
            obj.on_event(result)
        return True
