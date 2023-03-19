#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to run as telegram bot
"""
import core.emotions_engine as emotions_engine
from core.emotions_engine import EngineObserver
from core.emotions_engine import SentiMeterModule
import telebot
import os

BOT_TOKEN = os.environ.get("SENTI_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

EMOJI_HAPPY = "\U0001F600  "
EMOJI_SAD = "\U0001F622  "
EMOJI_FEAR = "\U0001F630  "
EMOJI_SURPRISE = "\U0001F914  "
EMOJI_ANGRY = "\U0001F620  "


class TelebotResponder(EngineObserver):
    def __init__(self, bot, message) -> None:
        self.message = message
        super().__init__("Telegrambot")
        emotions_engine.engine.add_observer(self)

    def on_event(self, message_text, emotion_map):
        global bot
        text = "| "
        total_emotions = sum(emotion_map.values())
        if total_emotions == 0:
            text = "I do not find any emotions :)"
        else:
            text += (
                EMOJI_ANGRY
                + str(((emotion_map["Angry"] / total_emotions) * 100))
                + " % | "
            )
            text += (
                EMOJI_FEAR
                + str(((emotion_map["Fear"] / total_emotions) * 100))
                + " % | "
            )
            text += (
                EMOJI_HAPPY
                + str(((emotion_map["Happy"] / total_emotions) * 100))
                + " % | "
            )
            text += (
                EMOJI_SAD + str(((emotion_map["Sad"] / total_emotions) * 100)) + " % | "
            )
            text += (
                EMOJI_SURPRISE
                + str(((emotion_map["Surprise"] / total_emotions) * 100))
                + " % |"
            )
        bot.reply_to(self.message, text)


class TelegramModule(SentiMeterModule):
    def __init__(self) -> None:
        super().__init__()

    def start(self):
        super().start()
        bot.infinity_polling()

    def stop(self):
        super().start()
        bot.stop()

    @bot.message_handler(func=lambda msg: True)
    def echo_all(message):
        print(message.text)
        t = TelebotResponder(bot, message)
        emotions_engine.engine.process_text(message.text)
        del t
