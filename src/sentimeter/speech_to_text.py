#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Speech to Text Module, Currently uses Google STT, Future we will add more offline Engines
"""
import logging
import speech_recognition as sr


class STTEngine:
    """
    Speech to Text Engine, Currently using Google Service, Options to be added for Sphinix
    """

    def __init__(self, recognizer) -> None:
        """
        constructor
        """
        self.recognizer = recognizer
        self.lang = "en-IN"
        pass

    def speech_to_text(self, audiodata):
        """
        function to get the text for inputed audio data
        """
        try:
            actual_result = self.recognizer.recognize_google(audiodata, language=self.lang, show_all=True)
        except sr.UnknownValueError:
            logging.fatal("Google Speech Recognition could not understand audio")
            exit(-1)
        except sr.RequestError as e:
            logging.fatal("Error service; {0}".format(e))
            exit(-1)
        if len(actual_result) == 0:
            logging.debug("Unable to get the Speech to Text,Ignoring")
            return ""

        # Lets get the best text
        if "confidence" in actual_result["alternative"]:
            # return alternative with highest confidence score
            best_hypothesis = max(
                actual_result["alternative"],
                key=lambda alternative: alternative["confidence"],
            )
        else:
            # when there is no confidence available, we arbitrarily choose the first hypothesis.
            best_hypothesis = actual_result["alternative"][0]
        result = best_hypothesis["transcript"]
        return result
