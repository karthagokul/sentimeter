
import emotions_engine
import telebot
import os
import json

from emotions_engine import EngineObserver
BOT_TOKEN = os.environ.get('SENTI_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

class TelebotResponder(EngineObserver):
    def __init__(self,bot,message) -> None:
        super().__init__("TelgramBot")
        
        self.message=message
        
    def update(self,message_text,emotions):
        print(emotions)
        print(message_text)
        global bot
       # bot.send_message(self.message.chat.id, message_text, parse_mode="Markdown")
       # bot.send_message(self.message.chat.id, json.dumps(emotions), parse_mode="Markdown")
        bot.reply_to(self.message, json.dumps(emotions))
        
        

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print(message.text)
    t=TelebotResponder(bot,message)
    emotions_engine.engine.bank.register(t)
    emotions_engine.engine.process_text(message.text)
    emotions_engine.engine.bank.unregister(t)
    del t

if __name__ == "__main__":
    bot.infinity_polling()