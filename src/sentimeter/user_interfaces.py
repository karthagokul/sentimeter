#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File which can handle various user interfaces , Currently only basic commandlines
"""

import sys
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QApplication,
    QVBoxLayout,
    QPlainTextEdit,
    QHBoxLayout,
    QLineEdit,
)

from threading import Thread
import core.emotions_engine as emotions_engine
from core.emotions_engine import EngineObserver


class SentimeterSimpleUI(EngineObserver):
    def __init__(self) -> None:
        super().__init__("Simple UI")
        emotions_engine.engine.add_observer(self)

    def on_event(self, message, emotions):
        print("Transcription")
        print(message)
        print("Emotions")
        print(emotions)


class SpinWithLabel(QWidget):
    def __init__(self, label):
        super().__init__()
        self.initUI(label)

    def initUI(self, label):
        self.value_wid = QLineEdit("0")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(label))
        layout.addWidget(self.value_wid)
        self.setLayout(layout)

    def update_spin(self, value):
        """
        Update emotional values
        """
        curval = float(self.value_wid.text())
        newval = curval + value
        repr_str = str(newval)
        self.value_wid.setText(repr_str)


class EmotionsIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        emotions_layout = QHBoxLayout()
        self.happy_widget = SpinWithLabel("Happy")
        self.sad_widget = SpinWithLabel("Sad")
        self.fear_widget = SpinWithLabel("Fear")
        self.angry_widget = SpinWithLabel("Angry")
        self.surprise_widget = SpinWithLabel("Surprise")
        emotions_layout.addWidget(self.happy_widget)
        emotions_layout.addWidget(self.sad_widget)
        emotions_layout.addWidget(self.fear_widget)
        emotions_layout.addWidget(self.angry_widget)
        emotions_layout.addWidget(self.surprise_widget)
        self.setLayout(emotions_layout)

    def update_emotions(self, emotions_map):
        if emotions_map["Happy"]:
            self.happy_widget.update_spin(emotions_map["Happy"])
        if emotions_map["Angry"]:
            self.angry_widget.update_spin(emotions_map["Angry"])
        if emotions_map["Surprise"]:
            self.surprise_widget.update_spin(emotions_map["Surprise"])
        if emotions_map["Sad"]:
            self.sad_widget.update_spin(emotions_map["Sad"])
        if emotions_map["Fear"]:
            self.fear_widget.update_spin(emotions_map["Fear"])


class SentiMeterWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.textarea = QPlainTextEdit("")
        layout = QVBoxLayout()
        self.emotions_indicator = EmotionsIndicator()

        layout.addWidget(self.textarea)
        layout.addWidget(self.emotions_indicator)

        self.setLayout(layout)
        self.show()

    def update(self, text, emotions):
        self.emotions_indicator.update_emotions(emotions)
        self.textarea.appendPlainText(text)


class SentiMeterGUI(EngineObserver):
    def __init__(self) -> None:
        self.thread = None
        self.widget = None
        super().__init__("Simple UI")
        emotions_engine.engine.add_observer(self)
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Sentimeter - Understands Emotions")

    def start(self, module):
        self.widget = SentiMeterWidget()
        # Start the Module in non GUI thread
        self.thread = Thread(target=module.start)
        self.thread.start()
        return self.app.exec()

    def on_event(self, message, emotions):
        self.widget.update(message, emotions)
