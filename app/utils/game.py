import os
from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4

path = os.path.dirname(os.path.abspath(__file__))


class Wordle:
    def __init__(self, word, chat_id, user_id, word_url):
        self.word = word.upper()
        self._word_url = word_url
        self._telegram_id = ""
        self.chat_id = chat_id
        self.user_id = user_id
        self.level = 0
        self.filename = "tiles-container.webp"
        self._board = Image.open(f"{path}/tiles-container.jpg")
        self._correct = Image.open(f"{path}/correct-background.jpg").resize(
            (43, 43), Image.LANCZOS
        )
        self._wrong = Image.open(f"{path}/wrong-background.jpg").resize(
            (43, 43), Image.LANCZOS
        )
        self._partial = Image.open(f"{path}/partially-correct-background.jpg").resize(
            (43, 43), Image.LANCZOS
        )
        self._font = ImageFont.truetype(f"{path}/Roboto-Regular.ttf", size=42)
        self._y = 11

    def verify_guess(self, guess):
        self._x = 11
        guess = guess.upper()
        if guess == self.word:
            for letter in self.word:
                self._board.paste(self._correct, (self._x, self._y))
                draw = ImageDraw.Draw(self._board)
                draw.text(
                    (self._x + 8, self._y - 2),
                    text=letter,
                    fill="white",
                    font=self._font,
                )
                self._x += 59
            self.filename = f"{str(uuid4())}.webp"
            self._board.save(f"{path}/{self.filename}")
            return True

        else:
            for index, letter in enumerate(guess):
                if letter == self.word[index]:
                    self._board.paste(self._correct, (self._x, self._y))
                elif letter in self.word and letter != self.word[index]:
                    self._board.paste(self._partial, (self._x, self._y))
                else:
                    self._board.paste(self._wrong, (self._x, self._y))
                draw = ImageDraw.Draw(self._board)
                draw.text(
                    (self._x + 8, self._y - 2),
                    text=letter,
                    fill="white",
                    font=self._font,
                )
                self._x += 59
        self._y += 58
        self.filename = f"{str(uuid4())}.webp"
        self._board.save(f"{path}/{self.filename}")
        self.level += 1
        return False
