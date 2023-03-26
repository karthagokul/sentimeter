# Sentimeter
![Alt text](https://github.com/karthagokul/sentimeter/blob/main/logo.png?raw=true  "Logo")

The module is published in pypi (https://pypi.org/project/sentimeter/) . you can install it via

    pip install sentimeter


## Introduction
Sentimeter is all about identifiying the sentiments from a source . The source can be a text / audio .
Below are some of the built in modules shipping along with the package .

### Audio Module
Process the Emotions in a given audio file. Currently it supports only wav file . In future we will add more formats
### Live Speech
Process the Emotions in a live speech
### Telegram Mode
Sentimeter has a Telegram Bot, it can process the emotions in a Telegram chat
### Text File
Process a text file and identifies the emotions
### Youtube Video
Under Development

Incase if you would like to create own modules, you can do it by extending the BaseSource class  like below


    class OwnSentimeterSource(BaseSource):
        def __init__(self, engine) -> None:
            super().__init__(engine)
            pass

        def run(self):
            # The text is is the input to the engine
            self.engine.process(text)
            return True

        def on_event(self, results):
            # This overridden function will get you the results(map of emotions)
            print(results)


We can use multiple backends as well with this engine. I have created an experimental ChatGPT backend . But by default it uses a built in model to identify the emotions.


## Class Diagram
![Alt text](https://github.com/karthagokul/sentimeter/blob/main/classes_sentimeter.png?raw=true  "Class Diagram")

## Package Diagram
![Alt text](https://github.com/karthagokul/sentimeter/blob/main/packages_sentimeter.png?raw=true  "Packages")

## Usage
There are applications developed using sentimeter. Please refer apps folder in https://github.com/karthagokul/sentimeter

## Todo
 - Documentation
 - Google Hangout Connector 
 
## Setup
Create a Virtual env

    py -m venv virtual-env
    .\virtual-env\Scripts\activate

Install All Dependencies

    pip3 install .
