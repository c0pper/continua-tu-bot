import logging
import os
import random
from time import sleep

import telegram.error
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, \
    ConversationHandler
# from text_generation import tokenizer, model, text_generator, prompt
from revChatGPT.V1 import Chatbot
print(os.environ.get('chatgpt_login'))
print(os.environ.get('chatgpt_pw'))
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8433'))
TELE_TOKEN = os.environ.get('TELE_TOKEN')

SENTENCE = range(1)
MIN_TEXT_LEN = 3

chatbot = Chatbot(config={
    "email": f"{os.environ.get('chatgpt_login')}",
    "password": f"{os.environ.get('chatgpt_pw')}"
})

# def generate_text(input_sentence):
#     output = text_generator(
#         input_sentence,
#         do_sample=True,
#         max_length=random.randint(100, 200),
#         top_k=50,
#         top_p=0.95,
#         num_return_sequences=1
#     )
#
#     return output


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


def chat_gpt_output_parser(prompt: str, update: Update, context: CallbackContext):
    reply = update.message.reply_text("Sto scrivendo...")
    gpt_out = ""
    for idx, data in enumerate(chatbot.ask(prompt)):
        if "continuazione" in prompt:
            start_msg = prompt.split("\n\n")[1]
            gpt_out = f'{start_msg} {data["message"]}'
        else:
            gpt_out = data["message"]
        if gpt_out:
            if idx % 30 == 0:
                try:
                    context.bot.editMessageText(chat_id=update.message.chat_id,
                                                message_id=reply.message_id,
                                                text=gpt_out)
                except telegram.error.BadRequest:
                    pass
    try:
        context.bot.editMessageText(chat_id=update.message.chat_id,
                                    message_id=reply.message_id,
                                    text=gpt_out)
    except telegram.error.BadRequest:
        pass


def continua_tu_chatGPT(update: Update, context: CallbackContext):
    input_sentence = update.message.text

    if len(input_sentence.split()) > MIN_TEXT_LEN:  # il testo è incluso dopo il comando
        if input_sentence[-3:] == "...":
            input_sentence = input_sentence[:-3]
        input_sentence = input_sentence.split(' ', 1)[1]
        prompt = f"Scrivi una continuazione di questo testo\n\n{input_sentence}"

        print(prompt)
        chat_gpt_output_parser(prompt, update, context)

    else:  # è stato scritto solo il comando
        update.message.reply_text("Uso del bot:")
        update.message.reply_text("'/continuatu Sono andato in bagno, quando all'improvviso'")


def get_replied_message_text(update: Update):
    """Handler for /start command"""
    if update.message.reply_to_message:
        input_text = update.message.reply_to_message["text"]
    else:
        input_text = ""
    return input_text


def parere_chatGPT(update: Update, context: CallbackContext):
    input_text = f"esprimi una critica su questo testo\n\n{get_replied_message_text(update)}"
    print("input:", input_text)
    print(update.message)
    if get_replied_message_text(update):
        chat_gpt_output_parser(input_text, update, context)
    else:
        update.message.reply_text("Rispondi al messaggio su cui vuoi in parere con /parere")


def main():
    """starting bot"""
    updater = Updater(TELE_TOKEN, use_context=True)

    # getting the dispatchers to register handlers
    dp = updater.dispatcher
    # registering commands
    dp.add_handler(CommandHandler("continuatu", continua_tu_chatGPT))
    dp.add_handler(CommandHandler("parere", parere_chatGPT))

    # starting the bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TELE_TOKEN,
    #                       webhook_url=HEROKU_URL + TELE_TOKEN)
    # updater.idle()


if __name__ == '__main__':
    main()
