import logging
from sentimeter.local_backend import LocalBackend

TEXT = "Text"


class Sentimeter:
    def __init__(self) -> None:
        self.backend = LocalBackend()
        self.__listeners = []
        self._enable_logging(logging.DEBUG)

    def _enable_logging(self, lev):
        logging.basicConfig(level=lev, format="[Sentimeter] [%(levelname)-5.5s]  %(message)s")

    def set_backend(self, backend):
        self.backend = backend
        logging.info("Switched to Backend " + self.backend.backend_name)

    def add_observer(self, listener):
        self.__listeners.append(listener)

    def remove_observer(self, listener):
        self.__listeners.remove(listener)

    def process(self, text):
        result = {}
        result = self.backend.process(text)
        result[TEXT] = text
        for obj in self.__listeners:
            obj.on_event(result)
        return True
