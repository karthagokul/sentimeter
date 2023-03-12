from intelli_speech import IntelliSpeech
import emotions_engine
from emotions_engine import EmotionsEngine
from threading import Thread
from time import sleep
import time
from rich.live import Live
from rich.table import Table
from rich import print
from rich.panel import Panel


class Sentimeter:
    listener = IntelliSpeech()
    display_timer = None
    active = False

    def __init__(self) -> None:
        emotions_engine.engine.run()

    def process_text(self, text_data):
        pass

    def process_text_file(self, file_name):
        pass

    def process_audio_file(self,file_name):
        self.__print_progress()
        self.listener.process_audio_file(file_name)

    def __print_progress(self):
        self.active = True
        self.display_timer = Thread(target=self.print).start()

    def __print_table(self):
        table = Table()
        table.add_column("Row ID")
        table.add_column("Description")
        table.add_column("Level")

        with Live(table, refresh_per_second=4) as live:  # update 4 times a second to feel fluid
            for row in range(12):
                live.console.print(f"Working on row #{row}")
                time.sleep(0.4)
                table.add_row(f"{row}", f"description {row}", "[red]ERROR")

    def print(self):
        # Create a basic Rich layout
        print(Panel("Hello, [red]World!"))
        while self.active:
            sleep(5)
            self.__print_table()
            #emotions_engine.engine.bank.print()

    def start_listening(self):
        if self.active:
            print("Another Listening is Ongoing")
            return 
        self.__print_progress()
        self.listener.listen()        
        


    def stop(self):
        print("Stopping Sentimeter")
        emotions_engine.engine.stop()
        if self.active:
            self.active = False
            self.listener.stop()
