"""
Class Description
"""
from rich import print
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.text import Text
from rich.table import Table, Column
from rich.live import Live
from emotions_engine import EngineObserver


class SentimeterUI(EngineObserver):
    console = Console()
    console.set_alt_screen(True)
    console.clear()
    layout = Layout()
    emotions_panel=Panel('')
    log_panel=Panel('')
    log_panel.title="Transcript"
    emotions_panel_layout=Layout()
    emotions_panel_happy=Panel('',title="Happy")
    emotions_panel_angry=Panel('',title="Angry")
    emotions_panel_surprise=Panel('',title="Surprise")
    emotions_panel_sad=Panel('',title="Sad")
    emotions_panel_fear=Panel('',title="Fear")

    def __init__(self) -> None:
        super().__init__("UI")
        self.emotions_panel_layout.split_row(
        self.emotions_panel_happy,
        self.emotions_panel_angry,
        self.emotions_panel_surprise,
        self.emotions_panel_sad,
        self.emotions_panel_fear
        )
        self.layout.split_column(
            Layout(self.emotions_panel_layout, ratio=4),
            Layout(self.log_panel, name="body", ratio=6)
        )
        live = Live(self.layout, refresh_per_second=1)
        live.start(refresh=True)
        self.log_panel.title="Transcript"
        self.emotions_panel.title= "Emotions"
    
    def update(self,message,emotions):
        self.update_emotions(emotions)
        self.update_transcript(message)
        
    def update_emotions(self,emotion_map):
        #Lets find percentage
        total_emotions=sum(emotion_map.values())
        if total_emotions==0:
            return
        self.emotions_panel_angry.renderable=str(((emotion_map["Angry"]/total_emotions)*100)) + " %"
        self.emotions_panel_fear.renderable=str(((emotion_map["Fear"]/total_emotions)*100)) + " %"
        self.emotions_panel_happy.renderable=str(((emotion_map["Happy"]/total_emotions)*100)) + " %"
        self.emotions_panel_sad.renderable=str(((emotion_map["Sad"]/total_emotions)*100)) + " %"
        self.emotions_panel_surprise.renderable=str(((emotion_map["Surprise"]/total_emotions)*100)) + " %"

    def update_transcript(self,transctipt):
        self.log_panel.renderable= transctipt

    def __del(self):
        self.console.clear()
