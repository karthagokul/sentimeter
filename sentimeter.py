import logging
from modules import LiveSpeechModule , TelegramModule , AudioModule
import signal
import sys
import click


#Module Global Instance
module=None
logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

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
    '''The Main function which process the user commands to start the respective modules'''
    global app
    global module
    if telegrambot == True:
        logging.info('Started Telegram Mode')
        module=TelegramModule()
    if live == True:
        logging.info('Started Listening Mode')
        module=LiveSpeechModule()  
    elif text != None:
        pass
    elif audio_file != None:
        logging.info("Process audio file")
        module=AudioModule(audio_file)  
    elif text_file != None:
        logging.info("Process text file")
    else:
        logging.fatal("Unable to Recognize")
    if module !=None:
        module.start()
    return

def signal_handler(sig, frame):
    ''' Need to capture the Control-C especially when any module is in live processing mode
    '''
    global module
    logging.info("Please wait, Let me cleanup")
    if module.is_active:
        module.stop()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    #Below line is required , Related to PY bug https://bugs.python.org/issue35935
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
