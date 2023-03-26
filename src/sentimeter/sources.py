#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from sentimeter.engine_observer import EngineObserver


class BaseSource(EngineObserver):
    def __init__(self, engine) -> None:
        """The Source Base class
        The class can be inherited to implement own run methods
        When a Source is created, it register with the engine as observer to process the events
        """
        # register to the app
        engine.add_observer(self)
        self.engine = engine
        pass

    def run(self):
        """'Do the Job / Eventloop"""
        pass

    def on_results(self, results):
        """Unused for now"""
        pass

    def on_event(self, results):
        """
        Observer Abstract Method
        """
        pass


class TextSource(BaseSource):
    """The simplest SentimeterSource
    The Instance can be created and executed with plain text
    """

    def __init__(self, engine) -> None:
        super().__init__(engine)
        pass

    def run(self, text):
        self.engine.process(text)
        return True

    def on_event(self, results):
        """Just print it"""
        logging.info(results)
