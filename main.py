import logging
import os
import datetime
import pytz

import telegram.error
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, \
    ConversationHandler
# from text_generation import tokenizer, model, text_generator, prompt
from revChatGPT.V3 import Chatbot
from utils import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8433'))
TELE_TOKEN = os.environ.get('TELE_TOKEN')

SENTENCE = range(1)
MIN_TEXT_LEN = 3




# Define Command Handlers
# def continua_tu(update: Update, context: CallbackContext):
#     """Handler for /start command"""
#     input_sentence = update.message.text
#     if len(input_sentence.split()) > MIN_TEXT_LEN:  # il testo è incluso dopo il comando
#         if input_sentence[-3:] == "...":
#             input_sentence = input_sentence[:-3]
#         update.message.reply_text("Sto scrivendo...")
#         input_sentence = input_sentence.split(' ', 1)[1]
#         print(input_sentence)
#         output = generate_text(input_sentence)
#         print(output)
#         update.message.reply_text(output[0]["generated_text"])
#     else:  # è stato scritto solo il comando
#         update.message.reply_text("Uso del bot:")
#         update.message.reply_text("'/continuatu Sono andato in bagno, quando all'improvviso'")


def continua_tu_chatGPT(update: Update, context: CallbackContext):
    """
    Handler for the /continuatu command. Generates a prompt to continue a given text.

    :param update: `telegram.Update` object representing an incoming update from Telegram.
    :param context: `telegram.ext.CallbackContext` object provided by the `telegram.ext` module.
    """
    # input_sentence = update.message.text
    input_sentence = get_replied_message_text(update)

    if len(input_sentence.split()) > MIN_TEXT_LEN:  # il testo è incluso dopo il comando
        # if input_sentence[-3:] == "...":
        #     input_sentence = input_sentence[:-3]
        # input_sentence = input_sentence.split(' ', 1)[1]
        prompt = f"Scrivi una continuazione di questo testo\n\n{input_sentence}"

        print(prompt)
        if update.message.from_user["id"] != 1748826398:
            chat_gpt_output_parser(prompt, update, context, input_sentence=input_sentence)
        else:
            time_is_valid = check_time(16, 18)
            if time_is_valid:
                chat_gpt_output_parser(prompt, update, context, input_sentence=input_sentence)
            else:
                update.message.reply_text("Lorenzo hai rotto")

    else:  # è stato scritto solo il comando
        update.message.reply_text("Rispondi a un messaggio con il comando /continuatu")



def parere_chatGPT(update: Update, context: CallbackContext):
    """
    Handler for the /parere command. Generates a prompt for the user to express a criticism of a given message, then
    passes it to the GPT-3 chatbot for generating a response.

    Args:
        update (:class:`telegram.Update`): The update object containing information about the incoming message.
        context (:class:`telegram.ext.CallbackContext`): The context object for handling the callback.

    Returns:
        None
    """
    input_text = f"esprimi una critica su questo testo:\n\n{get_replied_message_text(update)}"

    if get_replied_message_text(update):
        if update.message.from_user["id"] != id_valitutto:
            chat_gpt_output_parser(input_text, update, context)
        else:
            time_is_valid = check_time(start_time_valitutto, end_time_valitutto)
            if time_is_valid:
                chat_gpt_output_parser(input_text, update, context)
            else:
                update.message.reply_text("Lorenzo hai rotto")
    else:
        update.message.reply_text("Rispondi al messaggio su cui vuoi in parere con /parere")



def summarize(update: Update, context: CallbackContext, mode: str = "rules"):  # "ml" / "rules"
    """
    This function takes an Update and a CallbackContext object, and an optional mode string (defaulting to "rules")
    as input. It summarizes the text of the message replied to using the get_replied_message_text function and passes
    it to chat_gpt_output_parser for summarization. If the user is Lorenzo, the function will only work if the time
    is between 16:00 and 18:00. This function doesn't return anything, it just sends the summarized text as a reply.

    Args:
        update (telegram.Update): The update object.
        context (telegram.ext.CallbackContext): The context object.
        mode (str, optional): The summarization mode, either "rules" or "ml". Defaults to "rules".

    Returns:
        None
    """
    input_text = f"riassumi questo testo\n\n{get_replied_message_text(update)}"
    print("input:", input_text)
    if update.message.from_user["id"] != id_valitutto:
        chat_gpt_output_parser(input_text, update, context)
    else:
        time_is_valid = check_time(start_time_valitutto, end_time_valitutto)
        if time_is_valid:
            chat_gpt_output_parser(input_text, update, context)
        else:
            update.message.reply_text("Lorenzo hai rotto")



def key_points(update: Update, context: CallbackContext):
    input_text = f"Riporta in una lista i punti chiave di questo testo\n\n{get_replied_message_text(update)}"
    print("input:", input_text)
    if update.message.from_user["id"] != id_valitutto:
        chat_gpt_output_parser(input_text, update, context)
    else:
        time_is_valid = check_time(start_time_valitutto, end_time_valitutto)
        if time_is_valid:
            chat_gpt_output_parser(input_text, update, context)
        else:
            update.message.reply_text("Lorenzo hai rotto")


def main():
    """starting bot"""
    updater = Updater(TELE_TOKEN, use_context=True)

    # getting the dispatchers to register handlers
    dp = updater.dispatcher
    # registering commands
    dp.add_handler(CommandHandler("continuatu", continua_tu_chatGPT))
    dp.add_handler(CommandHandler("parere", parere_chatGPT))
    dp.add_handler(CommandHandler("riassunto", summarize))
    dp.add_handler(CommandHandler("puntichiave", key_points))

    # starting the bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TELE_TOKEN,
    #                       webhook_url=HEROKU_URL + TELE_TOKEN)
    # updater.idle()


if __name__ == '__main__':
    main()
