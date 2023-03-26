class Basebackend:
    """The Backend class, Abstract
    Provides an interface to engine to customize the backend
    """

    def __init__(self, backend_name) -> None:
        self.backend_name = backend_name

    def process(self, text):
        return {}
