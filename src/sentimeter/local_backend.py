import text2emotion as te
from sentimeter.backend import Basebackend


class LocalBackend(Basebackend):
    """The Backend which uses text2emotion module.
    TODO: Create own Spacy based emotion recognition
    """

    def __init__(self) -> None:
        """Constructor with a name"""
        super().__init__("Local")

    def process(self, text):
        """The Runner"""
        data = {}
        data = te.get_emotion(text)
        return data
