import text2emotion as te
#import nltk
#import pandas as pd
#from nltk import word_tokenize
#from nltk.stem.snowball import SnowballStemmer
#import requests
#nltk.download('punkt')

class EmotionChecker:
    def __init__(self) -> None:
        pass

    def process(self,text):
        return te.get_emotion(text)
    
    #return LeXmo.LeXmo(text)
    #Unsure if LeXmo is better