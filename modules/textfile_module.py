#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to Process a texfile
"""

import core.emotions_engine as emotions_engine
from core.emotions_engine import EngineObserver
from core.emotions_engine import SentiMeterModule


class TextFileModule(SentiMeterModule):
    def __init__(self, path) -> None:
        super().__init__()
        self.path = path

    def start(self):
        super().start()
        with open(self.path, "r") as fh:
            contents = fh.read()
            paragraphs = list(filter(lambda x: x != "", contents.split("\n\n")))
            # Lets process the emotions , paragraph by paragraph
            for paragrah in paragraphs:
                emotions_engine.engine.process_text(paragrah)

    def stop(self):
        super().stop()
