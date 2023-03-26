#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import signal

sys.path.append("..\src")
from sentimeter.sentimeter import Sentimeter
from sentimeter.live_speech_source import LiveSpeechSource


def main():
    instance = Sentimeter()
    audio_source = LiveSpeechSource(instance)
    audio_source.run()


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
