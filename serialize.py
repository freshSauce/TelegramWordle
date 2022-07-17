import os
from flask import request, Response
from actions import new_game, send_message, send_sticker


games = {}


def receive_info():
    if request.method == "POST":
        data = request.get_json(force=True)
        text, chat_id, chat_type, msg_id, user_id = getlastMsg(data)
        splitted_text = text.strip().split(" ")
        command = text.split(" ")[0]
        if len(splitted_text) >= 2:
            args = text.split(" ")[1:]
        else:
            args = []

        if command == "/newgame":
            game = new_game(chat_id, user_id)
            if not games.get(user_id):
                games[user_id] = game
                send_message(chat_id, msg_id, "¡Juego creado!", reply=True)
                send_sticker(chat_id, "tiles-container.webp")
            else:
                game = games[user_id]
                send_message(chat_id, msg_id, "!Tienes un juego en curso!", reply=True)
                send_sticker(chat_id, game.filename)
            return Response("Ok", 200)
        elif command == "/guess" and args:
            guess = args[0]
            if len(guess) != 5:
                send_message(
                    chat_id, msg_id, "¡Introduce una palabra de 5 letras!", reply=True
                )
            elif not games.get(user_id):
                send_message(
                    chat_id,
                    msg_id,
                    "¡Comienza creando un juego nuevo con /newgame!",
                    reply=True,
                )
            elif not guess.isalpha():
                send_message(
                    chat_id,
                    msg_id,
                    "¡Asegurate de usar únicamente letras!",
                    reply=True,
                )
            else:
                game = games[user_id]
                if game.verify_guess(guess):
                    send_sticker(chat_id, game.filename)
                    send_message(chat_id, msg_id, "¡Felicidades, ganaste!")
                    os.remove(game.filename)
                    games[user_id] = ""
                else:
                    if game.level != 6:
                        send_sticker(chat_id, game.filename)
                        send_message(chat_id, msg_id, "¡Sigue intentando!")
                        os.remove(game.filename)
                    else:
                        send_sticker(chat_id, game.filename)
                        send_message(chat_id, msg_id, "¡Has perdido!")
                        os.remove(game.filename)
                        games[user_id] = ""
                        send_message(chat_id, msg_id, f"La palabra era {game.word}")
        return Response("Ok", 200)

    else:
        return "Test"


def getlastMsg(msg):
    if msg.get("message"):
        chat_id = msg.get("message").get("chat").get("id")
        text = msg.get("message").get("text")
        chat_type = msg["message"]["chat"]["type"]
        msg_id = msg["message"]["message_id"]
        user_id = msg["message"]["from"]["id"]
    else:
        chat_id = msg.get("edited_message").get("chat").get("id")
        text = msg.get("edited_message").get("text")
        chat_type = msg["edited_message"]["chat"]["type"]
        msg_id = msg["edited_message"]["message_id"]
        user_id = msg["edited_message"]["from"]["id"]

    return text, chat_id, chat_type, msg_id, user_id
