import text2emotion as te
from sentimeter.backend import Basebackend


class LocalBackend(Basebackend):
    def __init__(self) -> None:
        super().__init__("Local")

    def process(self, text):
        data = {}
        data = te.get_emotion(text)
        return data
