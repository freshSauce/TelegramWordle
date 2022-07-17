from app.utils.game import Wordle
from app.utils.config import API_KEY

import os
from random import choice, randint
from csv import DictReader

import logging
import requests as r

path = os.path.dirname(os.path.abspath(__file__))
API_URL = f"https://api.telegram.org/bot{API_KEY}"


def select_word():
    with open(f"{path}/data.csv", mode="r", newline="", encoding="utf8") as file:
        reader = DictReader(file)
        word = choice(list(reader))
        return word


def send_message(chat_id, message_id, message, reply=False, parse_mode="Markdown "):
    if reply:
        data = {
            "chat_id": chat_id,
            "reply_to_message_id": message_id,
            "text": message,
            "parse_mode": parse_mode,
        }
    else:
        data = {"chat_id": chat_id, "text": message, "parse_mode": parse_mode}

    api_result = r.get(f"{API_URL}/sendMessage", data=data)

    if api_result.status_code != 200:
        logging.error(
            f"Error: {api_result.json()['description']} while sending message."
        )


def send_sticker(chat_id, filename=None, reuse=False, file_id=None):
    if not reuse:
        sticker = open(f"{path}/{filename}", "rb")
        api_result = r.get(
            f"{API_URL}/sendSticker?chat_id={chat_id}", files={"sticker": sticker}
        )
    else:
        api_result = r.get(f"{API_URL}/sendSticker?chat_id={chat_id}&sticker={file_id}")

    if api_result.status_code != 200:
        ...
        logging.error(
            f"Error: {api_result.json()['description']} while sending sticker."
        )
    return api_result.json()["result"]["sticker"]["file_id"]


def new_game(chat_id, user_id):
    word = select_word()
    game = Wordle(word["title"], chat_id, user_id, word["url"])
    return game


def returnNLengthNumber(n):
    number = ""
    for _ in range(n):
        number += str(randint(0, 9))

    return int(number)
