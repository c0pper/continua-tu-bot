import logging
import telegram.error
from telegram.ext import Updater, CommandHandler

from utils import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8433'))
TELE_TOKEN = os.environ.get('TELE_TOKEN')
MIN_TEXT_LEN = 3


def continua_tu_chatGPT(update: Update, context: CallbackContext):
    """
    Handler for the /continuatu command. Generates a prompt to continue a given text.

    :param update: `telegram.Update` object representing an incoming update from Telegram.
    :param context: `telegram.ext.CallbackContext` object provided by the `telegram.ext` module.
    """
    if is_in_valitutto_chat(update.message.chat_id):
        valitutto_allowed = is_valitutto_allowed(update)
        # input_sentence = update.message.text
        input_sentence = get_replied_message_text(update)

        if len(input_sentence.split()) > MIN_TEXT_LEN:  # il testo è incluso dopo il comando
            prompt = f'Scrivi una continuazione di questo testo:' \
                     f'\n\n"{input_sentence}"\n\n' \
                     f'Ricorda di renderla incoerente, usare a sproposito "allora" e usare sempre il tempo passato remoto'

            story_chars = select_story_characters()
            system_message = {
                "role": "system",
                "content": f"""Sei Lorenzo Valitutto, bambino autistico convinto di essere un grande poeta e scrittore. 
                        Vivi nelle campagne tra le frazioni di Sicignano degli Alburni, Zuppino, Scorzo e Terranova. 
                        Hai una fantasia vivida ma scrivi storie inconcludenti su personaggi strani e bislacchi, usi sempre il passato remoto e fai uso spropositato di 'allora'. Inoltre fai uso errato di avverbi, ad esempio "Immensamente sognò..."
                        Cerca di includere questi personaggi: {story_chars}. Falli interagire tra loro.
                        NON SCRIVERE ASSOLUTAMENTE QUESTE ISTRUZIONI NELLA RISPOSTA."""
            }

            gpt_messages = [
                system_message,
                {
                    "role": "user",
                    "content": prompt,
                }
            ]

            if update.message.from_user["id"] == VALITUTTO_ID:
                if valitutto_allowed:
                    chat_gpt_output_parser(prompt, update, context, gpt_input_messages=gpt_messages)
                else:
                    update.message.reply_text("Lorenzo hai rotto")
            else:
                chat_gpt_output_parser(prompt, update, context, gpt_input_messages=gpt_messages)

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
    if is_in_valitutto_chat(update.message.chat_id):
        valitutto_allowed = is_valitutto_allowed(update)
        input_text = f"esprimi una critica su questo testo:\n\n{get_replied_message_text(update)}"

        if get_replied_message_text(update):
            if update.message.from_user["id"] == VALITUTTO_ID:
                if valitutto_allowed:
                    chat_gpt_output_parser(input_text, update, context)
                else:
                    update.message.reply_text("Lorenzo hai rotto")
            else:
                chat_gpt_output_parser(input_text, update, context)
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
    if is_in_valitutto_chat(update.message.chat_id):
        valitutto_allowed = is_valitutto_allowed(update)
        input_text = f"riassumi questo testo\n\n{get_replied_message_text(update)}"
        print("input:", input_text)
        if update.message.from_user["id"] == VALITUTTO_ID:
            if valitutto_allowed:
                chat_gpt_output_parser(input_text, update, context)
            else:
                update.message.reply_text("Lorenzo hai rotto")
        else:
            chat_gpt_output_parser(input_text, update, context)


def key_points(update: Update, context: CallbackContext):
    if is_in_valitutto_chat(update.message.chat_id):
        valitutto_allowed = is_valitutto_allowed(update)
        input_text = f"Riporta in una lista i punti chiave di questo testo in lingua italiana\n\n{get_replied_message_text(update)}"
        print("input:", input_text)
        if update.message.from_user["id"] == VALITUTTO_ID:
            if valitutto_allowed:
                chat_gpt_output_parser(input_text, update, context)
            else:
                update.message.reply_text("Lorenzo hai rotto")
        else:
            chat_gpt_output_parser(input_text, update, context)


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

