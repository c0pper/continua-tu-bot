import logging
import os
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, \
    ConversationHandler
from text_generation import tokenizer, model, text_generator, prompt

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

HEROKU_URL = "https://zettibot-witai.herokuapp.com/"
PORT = int(os.environ.get('PORT', '8433'))
TELE_TOKEN = "2111353739:AAFecNyq2fsvyahJCBMhJ8RNTlkXupCsrBA"  # os.environ.get('TELE_TOKEN')

SENTENCE = range(1)

min_text_lenght = 3


def generate_text(input_sentence):
    output = text_generator(
        input_sentence,
        do_sample=True,
        max_length=random.randint(100, 200),
        top_k=50,
        top_p=0.95,
        num_return_sequences=1
    )

    return output


# Define Command Handlers
def continua_tu(update: Update, context: CallbackContext):
    """Handler for /start command"""
    input_sentence = update.message.text
    if len(input_sentence.split()) > min_text_lenght:  # il testo è incluso dopo il comando
        if input_sentence[-3:] == "...":
            input_sentence = input_sentence[:-3]
        input_sentence = input_sentence + " "
        update.message.reply_text("Sto scrivendo...")
        input_sentence = input_sentence.split(' ', 1)[1]
        print(input_sentence)
        output = generate_text(input_sentence)
        print(output)
        update.message.reply_text(output[0]["generated_text"])
    else:  # è stato scritto solo il comando
        update.message.reply_text("Uso del bot:")
        update.message.reply_text("'/continuatu Sono andato in bagno, quando all'improvviso'")


def main():
    """starting bot"""
    updater = Updater(TELE_TOKEN, use_context=True)

    # getting the dispatchers to register handlers
    dp = updater.dispatcher
    # registering commands
    dp.add_handler(CommandHandler("continuatu", continua_tu))

    # starting the bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TELE_TOKEN,
    #                       webhook_url=HEROKU_URL + TELE_TOKEN)
    # updater.idle()


if __name__ == '__main__':
    main()
