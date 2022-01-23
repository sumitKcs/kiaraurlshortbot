from telegram.ext import Updater, CommandHandler
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import requests
import json
import logging
import os

TOKEN = '5254089086:AAG6O7913WDe_j7dm7jFUCW42PGXj6Gvmcc'

PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hey! I am Kiara, a URL Shortener Bot. Send me your long URL and I'll short it for you.")


def get_url(link):
    try:
        url = "https://api.shrtco.de/v2/shorten?url="+link
        response = requests.request("GET", url)
        response = json.loads(response.text)
        short_url = response["result"]["short_link"]
        return short_url
    except Exception as e:
        print(e)

def short(update: Update, context: CallbackContext):
    data = get_url(update.message.text)
    if data:
        update.message.reply_text("Here is your shorted url: 👇\n"+data)

   #https://api.telegram.org/bot5254089086:AAG6O7913WDe_j7dm7jFUCW42PGXj6Gvmcc/getMe


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, short))
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    updater.bot.set_webhook("https://kiaraurlshortbot.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()