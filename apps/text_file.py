import sys
import os

sys.path.append("..\src")
from sentimeter.sentimeter import Sentimeter
from sentimeter.sources import TextSource
from sentimeter.chatgpt_backend import AIRemoteBackend

CHATGPT_KEY = os.environ.get("OPENAI_KEY")

app = Sentimeter()
# By default the app uses a local backend.We can use ChatGPT also as backend
backend = AIRemoteBackend(CHATGPT_KEY)
app.set_backend(backend)
source = TextSource(app)
# source.run("OpenAI is such an amazing thing , i really do not know how it works , It makes life easier")
source.run("I am down with fever, Its really annoying")
