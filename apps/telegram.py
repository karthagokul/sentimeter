#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
import os
import logging
import telebot

sys.path.append("..\src")
from sentimeter.sentimeter import Sentimeter
from sentimeter.engine_observer import EngineObserver
from sentimeter.sources import BaseSource

CHATGPT_KEY = os.environ.get("OPENAI_KEY")


class TelebotResponder(EngineObserver):
    """Class which responds to a message with the emotions found in the message"""

    def __init__(self, engine, bot, message) -> None:
        self.message = message
        super().__init__("Telegrambot")
        self.bot = bot
        self.engine = engine
        engine.add_observer(self)

    def on_event(self, emotion_map):
        text = ""
        logging.debug(emotion_map)
        for x in emotion_map:
            if x != "Text":
                text += x + " : " + str(emotion_map[x])
                text += " , "
        logging.info(text)
        self.bot.reply_to(self.message, text)
        self.engine.remove_observer(self)


class SentimeterTelegramBot(BaseSource):
    """Custom Telegram Source and register it with Engine"""

    def __init__(self, engine, bot_key) -> None:
        super().__init__(engine)
        self.bot = telebot.TeleBot(bot_key)
        self.engine = Sentimeter()

    def run(self):
        """Runner"""

        @self.bot.message_handler(commands=["start"])
        def send_welcome(message):
            self.bot.reply_to(message, "Welcome to my bot!")

        @self.bot.message_handler(func=lambda msg: True)
        def echo_all(message):
            logging.info("Got message" + message.text)
            responder = TelebotResponder(self.engine, self.bot, message)
            self.engine.process(message.text)

        self.bot.infinity_polling()


def main():
    """The main"""
    if len(sys.argv) < 2:
        logging.critical("Error : Bot KEY must be presented")
        sys.exit(-1)
    bot_key = sys.argv[1]
    instance = Sentimeter()
    module = SentimeterTelegramBot(instance, bot_key)
    return module.run()


def signal_handler(sig, frame):
    """for safe exit ctrl-c"""
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
