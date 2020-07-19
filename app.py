import logging
from flask import Flask, request
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from utlis import get_reply,fetch_news,topics_keyboard

#enable logging
logging.basicConfig(format='%(asctime)s - %(leveltime)s - %(message)s',level=logging.INFO)
logger=logging.getLogger(__name__)

TOKEN="1139147319:AAHkpfMX3kSaXn93Donsq0FG76wTMFt6cao"

app=Flask(__name__)

@app.route('/')
def index():
    return "hello!"

@app.route(f'/{TOKEN}',methods=['GET','POST'])
def webhook():
    '''webhook view which recieves updates from telegram'''
    #create update object from json-format request data
    update= Update.de_json(request.get_json(), bot)
    #process update
    dp.process_update(update)
    return "ok"


def start(bot,update):
    print(update)
    author=update.message.from_user.first_name
    #msg=update.message.text  not using this because we already know the command
    reply="Hi! {}".format(author)
    bot.send_message(chat_id=update.message.chat_id,text=reply)
    
def help(bot,update):
    help_text="hey it is help text"
    bot.send_message(chat_id=update.message.chat_id,text=help_text)
def news(bot, update):
    bot.send_message(chat_id=update.message.chat_id,text="Choose a Category",
    reply_markup= ReplyKeyboardMarkup(keyboard=topics_keyboard,one_time_keyboard=True))


def reply_text(bot,update):
    intent,reply=get_reply(update.message.text,update.message.chat_id)
    if intent =="get_news":
        articles= fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id=update.message.chat_id,text=article["link"])
    else:
        bot.send_message(chat_id=update.message.chat_id,text=reply)

def echo_sticker(bot,update):
    bot.send_sticker(chat_id=update.message.chat_id,sticker=update.message.sticker.file_id)

def error(bot,update):
    logger.error("update'%s' caused error '%s'",update,update.error)


bot=Bot(TOKEN)
try:
    bot.set_webhook("https://dry-coast-01059.herokuapp.com/"+TOKEN)
except Exception as e:
    print(e)
    
dp=Dispatcher(bot,None)
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",help))
dp.add_handler(CommandHandler("news",news))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_error_handler(error)
    
#creating an entry for the program
if __name__=="__main__":
    app.run(port=8443)