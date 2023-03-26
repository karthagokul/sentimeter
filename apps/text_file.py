import sys
import os

sys.path.append("..\src")
from sentimeter.sentimeter import Sentimeter
from sentimeter.sources import TextSource

instance = Sentimeter()

# from sentimeter.chatgpt_backend import AIRemoteBackend
# CHATGPT_KEY = os.environ.get("OPENAI_KEY")
# Lets create the instance
# By default the app uses a local backend.We can use ChatGPT also as backend
# backend = AIRemoteBackend(CHATGPT_KEY)
# Set the experimental engine as backend
# instance.set_backend(backend)
# start the process

source = TextSource(instance)
source.run("I am down with fever, Its really annoying")
