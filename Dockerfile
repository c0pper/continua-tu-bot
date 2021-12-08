FROM python:3

ADD main.py /

RUN pip install transformers python-telegram-bot

CMD [ "python", "./main.py" ]