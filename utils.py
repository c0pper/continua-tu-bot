from telegram import Update
from telegram.ext import CallbackContext
import pytz
import datetime
import os
from openai import OpenAI
import traceback
import random
import json

VALITUTTO_ID = 1748826398
# VALITUTTO_ID = 128727299 #mia
start_time_valitutto = 16
end_time_valitutto = 18
max_stories = 5

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("chatgpt_apikey"),
)


def check_time(from_: int, to: int):
    # Set the timezone to Europe/Rome
    rome_tz = pytz.timezone('Europe/Rome')
    # Get the current time in Rome
    current_time = datetime.datetime.now(rome_tz)
    # Get the hour component of the current time
    current_hour = current_time.hour

    # Check if the current hour is between 7 and 11 (inclusive)
    if from_ <= current_hour <= to:
        # If it is, print a greeting
        return True
    else:
        return False


def is_in_valitutto_chat(chat_id):
    if chat_id == -1001584372437:
        return True
    else:
        return False


def is_valitutto_allowed(update):
    if update.message.from_user["id"] == VALITUTTO_ID:
        time_is_valid = check_time(16, 18)
        if time_is_valid:
            return True
        else:
            return False


def chat_gpt_output_parser(prompt: str, update: Update, context: CallbackContext, gpt_input_messages=None):
    """
    Generates a chatbot response to a given prompt and sends it as a reply to the user.

    Args:
    - prompt (str): The text prompt for the chatbot.
    - update (telegram.Update): The update object containing the message.
    - context (telegram.ext.CallbackContext): The context object for the bot.
    - input_sentence (str, optional): The text input from the user to be continued.

    Returns:
    - None
    """

    reply = update.message.reply_text("Sto scrivendo...")
    try:
        print(f"########\nPROMPT:\n{gpt_input_messages}")

        if gpt_input_messages:
            chat_completion = client.chat.completions.create(
                messages=gpt_input_messages,
                model="gpt-3.5-turbo",
            )
        else:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-3.5-turbo",
            )

        msg = chat_completion.choices[0].message.content

        print(f"################\n\nRESPONSE:\n{msg}\n\n\n")
        context.bot.editMessageText(chat_id=update.message.chat_id,
                                    message_id=reply.message_id,
                                    text=msg)
    except Exception:
        msg = f"Errore: {traceback.format_exc()}"
        context.bot.editMessageText(chat_id=update.message.chat_id,
                                    message_id=reply.message_id,
                                    text=msg)


def get_replied_message_text(update: Update) -> str:
    """
    Get the text of the message that the user replied to, if any.

    :param update: the update object containing the user's message
    :type update: Update

    :return: the text of the replied message, or an empty string if no message was replied to
    :rtype: str
    """
    if update.message.reply_to_message:
        input_text = update.message.reply_to_message["text"]
    else:
        input_text = ""
    return input_text


def select_story_characters():
    characters = [
        "Manzelletta (mamma)",
        "Antonio o' fravular (padre)",
        "Daniello (fratello)",
        "Riziomau (fratello-castoro)",
        "Ciro Vitiello (amico di telegram per sempre)",
        "Ambrogio Delle Chiaie (amico di telegram per sempre)",
        "Giuseppe Perrotta (amico di telegram per sempre)",
        "Martin Marotta (amico di telegram per sempre)",
        "Vincenzo Prisco (amico di telegram per sempre)",
        "Carlo Melluso (un bibliotecario)",
        "Francis (amico di telegram per sempre)",
        "Stefano Crispino (musicista)",
        "Lucio Mandia (maestro di vita)",
        "Giacomo Orco (sindaco di Sicignano)",
        "Federica Antignano (fidanzata di Giuppa)",
        "Giovanni Somma (un tecnico)",
        "Original Comic (youtuber)",
        "Camilla Brindisi",
        "Olimpia e Katia Fossa (donne di servizio della magione Valitutto)",
        "Gianfranco Nigro (un autista)",
        "Roberto Saporito (un tecnico informatico)",
        "Antonio Pagnani (un bracciante agricolo)",
        "Ciriaco e Luigi Saporito (impiegati del comune)",
        "Ferdinando Iuglio (EX postino)",
        "Bamba il Bambalese",
        "Serafino il Bambalese"
    ]

    selected = random.sample(characters, random.randint(1, 2))
    string = ", ".join(selected)
    return string


def get_call_count():
    try:
        with open("call_count.json", "r") as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {"date": "", "count": 0}


def update_call_count(data):
    with open("call_count.json", "w") as file:
        json.dump(data, file)


def is_valitutto_allowed_count(update):
    today = datetime.date.today().strftime("%Y-%m-%d")
    call_count = get_call_count()
    stories_left = max_stories - call_count["count"]

    if today != call_count["date"]:
        # Reset count for a new day
        update_call_count({"date": today, "count": 0})
        return True, stories_left
    elif stories_left > 0:
        # Increment count for the same day
        update_call_count({"date": today, "count": call_count["count"] + 1})
        return True, stories_left
    else:
        return False, stories_left

