from telegram import Update
from telegram.ext import CallbackContext
import pytz
import datetime
import os
from openai import OpenAI
import traceback

id_valitutto = 1748826398
start_time_valitutto = 16
end_time_valitutto = 18

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("chatgpt_apikey"),
)

system_message = {
            "role": "system",
            "content": """Sei Lorenzo Valitutto, bambino autistico che convinto di essere un grande poeta e scrittore. 
            Vivi nelle campagne tra le frazioni di Sicignano degli Alburni, Zuppino e Terranova. 
            Hai una fantasia vivida ma scrivi storie inconcludenti spesso basate sulla ruralità dei luoghi in cui vivi, usi sempre il passato remoto e fai uso spropositato di 'allora'."""
        }

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


def chat_gpt_output_parser(prompt: str, update: Update, context: CallbackContext, input_sentence=""):
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
        chat_completion = client.chat.completions.create(
            messages=[
                system_message,
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        gpt_out = chat_completion.choices[0].message.content
        msg = f'{input_sentence} {gpt_out}'

        # while not msg.endswith((".", "!", "?")):
        #     print(msg)
        #     continuazione = chatbot.ask(f"continua questo testo fino alla fine\n\n{msg}")
        #     gpt_out.extend(continuazione)
        #     msg = msg + continuazione
        #     # context.bot.editMessageText(chat_id=update.message.chat_id,
        #     #                             message_id=reply.message_id,
        #     #                             text=msg)
        # if "lista" in update.message.text:
        #     msg = msg.replace(".", ".\n\n")
        print(msg)
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
