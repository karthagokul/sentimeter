from sentimeter.sentimeter import Sentimeter
from sentimeter.sources import TextSource

app = Sentimeter()
source = TextSource(app)
source.run("I am down with fever, Its really annoying")
