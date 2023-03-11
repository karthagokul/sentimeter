
import signal
import sys
from sentimeter import Sentimeter

app=Sentimeter()

def signal_handler(sig, frame):
    print('Please wait, Let me cleanup')
    app.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    app.start()