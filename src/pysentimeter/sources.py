from pysentimeter.sentimeter import EngineObserver


class BaseSource(EngineObserver):
    def __init__(self, engine) -> None:
        """ """
        # register to the app
        engine.add_observer(self)
        self.engine = engine
        pass

    def run(self):
        """'Do the Job / Eventloop"""
        pass

    def on_results(self, results):
        pass

    def on_event(self, results):
        """
        Observer Abstract Method
        """
        pass


class LiveSpeechSource(BaseSource):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        pass

    def run(self):
        return True

    def on_event(self, results):
        pass


class TextSource(BaseSource):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        pass

    def run(self, text):
        self.engine.process(text)
        return True

    def on_event(self, results):
        print(results)
