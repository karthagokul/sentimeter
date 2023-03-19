import logging
from intelli_audio import IntelliAudio
import signal
import sys
import click
from user_interfaces import SentimeterSimpleUI
# from user_interfaces import SentimeterUI


class Sentimeter:
    '''
    The Application class
    '''
    listener = IntelliAudio()

    def __init__(self) -> None:
        '''Constructor'''
        pass

    def process_text(self, text_data):
        '''
        Process Given Text data
        '''
        pass

    def process_text_file(self, file_name):
        '''
        Process a Text file
        '''
        # ui=SentimeterUI()
        pass

    def process_audio_file(self, file_name):
        '''
        Process Audio File
        '''
        ui = SentimeterSimpleUI("AudioProcessingUI")
        self.listener.process_audio_file(file_name)

    def start_listening(self):
        '''
        Process Live Speech from Microphone
        '''
        # ui=SentimeterUI()
        return self.listener.listen()

    def stop(self):
        '''
        Stops Engine
        '''
        self.listener.stop()
        return



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
