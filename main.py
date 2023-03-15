import signal
import sys
from sentimeter import Sentimeter
import click

app = Sentimeter()


@click.command()
@click.option(
    "--live", is_flag=True, default=False, help="Application in Live Listening Mode"
)
@click.option("--text", help="Text to Process")
@click.option("--audio_file", help="Process Audio File")
@click.option("--text_file", help="File to Process")
def main(live, text, audio_file, text_file):
    signal.signal(signal.SIGINT, signal_handler)
    global app
    if live == True:
        print("Live")
        app.start_listening()
    elif text != None:
        click.echo("Hello %s!" % text)
        #app.process_text(text)
    elif audio_file != None:
        print("Process audio file")
        app.process_audio_file(audio_file)
    elif text_file != None:
        print("Process text file")
    return


def signal_handler(sig, frame):
    #global app
    print("Please wait, Let me cleanup")
    app.stop()
    sys.exit(0)


if __name__ == "__main__":
    main()
