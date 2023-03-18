"""
Class Description
"""

from sentimeter import Sentimeter
import signal
import sys
import click
import logging
logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')


app = Sentimeter()

@click.command()
@click.option(
    "--live", is_flag=True, default=False, help="Application in Live Listening Mode"
)
@click.option(
    "--telegrambot", is_flag=True, default=False, help="Application in Acting as a Telegram Bot"
)
@click.option("--text", help="Text to Process")
@click.option("--audio_file", help="Process Audio File")
@click.option("--text_file", help="File to Process")

def main(live,telegrambot, text, audio_file, text_file):
    global app
    if telegrambot == True:
        logging.info('Started Telegram Mode')
    if live == True:
        logging.info('Started Listening Mode')
        app.start_listening()
    elif text != None:
        pass
        #app.process_text(text)
    elif audio_file != None:
        logging.info("Process audio file")
        app.process_audio_file(audio_file)
    elif text_file != None:
        logging.info("Process text file")
    else:
        logging.fatal("Unable to Recognize")
    return

def signal_handler(sig, frame):
    #global app
    logging.info("Please wait, Let me cleanup")
    app.stop()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    #Below line is required , Related to PY bug https://bugs.python.org/issue35935
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
