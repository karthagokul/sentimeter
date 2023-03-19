#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File which can handle various user interfaces , Currently only basic commandlines
"""
import core.emotions_engine as emotions_engine
from core.emotions_engine import EngineObserver


class SentimeterSimpleUI(EngineObserver):
    def __init__(self, name) -> None:
        super().__init__(name)
        emotions_engine.engine.add_observer(self)

    def on_event(self, message, emotions):
        print("Transcription")
        print(message)
        print("Emotions")
        print(emotions)
