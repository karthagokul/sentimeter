
# sentimeter

Sentimeter is an app written in python to understand the emotions in audio / text. Currently it has the below modules
* Audio Module
 Process the Emotions in a given audio file. Currently it supports only wav file . In future we will add more formats

* Live Speech
Process the Emotions in a live speech

* Telegram Mode
Sentimeter has a Telegram Bot, it can process the emotions in a Telegram chat

* Text File
Process a text file and identifies the emotions

* Youtube Video
Under Development




## Usage

    python main.py --live to use live speech as source
    python main.py --audio_file <path  to  the  audio  file> to use as source

## Todo
* Documentation
* Google Hangout Connector
* Convert the Observer Pattern through Decorator

![Alt text](classes_sentimeter.png?raw=true "Design")
![Alt text](packages_sentimeter.png?raw=true "Design") 

## Setup

py -m venv virtual-env

.\virtual-env\Scripts\activate

pip install -r requirements.txt

pyreverse -o png -p sentimeter .