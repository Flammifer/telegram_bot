from telegram import *
from token_file import mytoken
from telegram.ext import *



class MyBot:
    def __init__(self, mytoken, logicHandler, startHandler):
        self.updater = Updater(token=mytoken, use_context=True)
        self.dispatcher = self.updater.dispatcher
        start_handler = CommandHandler('start', startHandler)
        self.dispatcher.add_handler(start_handler)
        logic_handler = MessageHandler(Filters.text, logicHandler)
        self.dispatcher.add_handler(logic_handler)
        self.updater.start_polling()
        print('-----Core is loaded-----')


class Utilities:
    def __init__(self, bot = None, context = None, update = None):
        self.bot = bot
        self.context = context
        self.update = update
        
            
