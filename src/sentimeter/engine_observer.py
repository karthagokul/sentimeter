class EngineObserver:
    def __init__(self, name) -> None:
        """
        A Name is given for observer
        """
        self.name = name

    def on_event(self, results):
        """
        Observer Abstract Method
        """
        pass
