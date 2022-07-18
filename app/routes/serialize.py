import os
import shelve
from flask import request, Response
from app.utils.start_message import message as start_message
from app.utils.actions import new_game, send_message, send_sticker, path


def receive_info():
    if request.method == "POST":
        data = request.get_json(force=True)
        text, chat_id, chat_type, msg_id, user_id = getlastMsg(data)
        if text is None:
            return Response("Ok", 200)
        splitted_text = text.strip().split(" ")
        command = text.split(" ")[0]
        if len(splitted_text) >= 2:
            args = text.split(" ")[1:]
        else:
            args = []
        with shelve.open("games") as games:
            if command == "/newgame":
                if not games[user_id]:
                    print(games)
                    game = new_game(chat_id, user_id)
                    games[user_id] = game
                    send_message(chat_id, msg_id, "¡Juego creado!", reply=True)
                    file_id = send_sticker(chat_id, filename="tiles-container.webp")
                    game._telegram_id = file_id
                else:
                    game = games[user_id]
                    send_message(
                        chat_id, msg_id, "¡Tienes un juego en curso!", reply=True
                    )
                    send_sticker(chat_id, reuse=True, file_id=game._telegram_id)
            elif command == "/guess" and args:
                guess = args[0]
                if len(guess) != 5:
                    send_message(
                        chat_id,
                        msg_id,
                        "¡Introduce una palabra de 5 letras!",
                        reply=True,
                    )
                elif not games[user_id]:
                    print(games)
                    print(user_id)
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
                        send_message(chat_id, msg_id, "¡Felicidades, ganaste!")
                        os.remove(f"{path}/{game.filename}")
                        del games[user_id]
                    else:
                        if game.level != 6:
                            file_id = send_sticker(chat_id, filename=game.filename)
                            game._telegram_id = file_id
                            send_message(chat_id, msg_id, "¡Sigue intentando!")
                            os.remove(f"{path}/{game.filename}")
                        else:
                            send_sticker(chat_id, filename=game.filename)
                            send_message(chat_id, msg_id, "¡Has perdido!")
                            os.remove(f"{path}/{game.filename}")
                            del games[user_id]
                            send_message(chat_id, msg_id, f"La palabra era {game.word}")
            elif command == "/giveup":
                send_message(
                    chat_id, msg_id, "Una lástima ;( ¡Mejor suerte a la próxima!"
                )
                del games[user_id]
            elif command == "/start" or command == "/help":
                send_message(chat_id, msg_id, start_message)
            games.close()
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
