#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import signal
import logging

sys.path.append("..\src")

from sentimeter.sentimeter import Sentimeter
from sentimeter.file_audio_source import AudioSource
from sentimeter.backends import AIRemoteBackend

CHATGPT_KEY = os.environ.get("OPENAI_KEY")


def main():
    if len(sys.argv) < 2:
        logging.critical("Error : Audio filename must be provided")
        sys.exit(-1)
    app = Sentimeter()
    backend = AIRemoteBackend(CHATGPT_KEY)
    app.set_backend(backend)
    audio_source = AudioSource(app, sys.argv[1])
    audio_source.run()


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
