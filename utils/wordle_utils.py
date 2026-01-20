import requests
from db.dao import check_word_in_db
from typing import Optional, List
from settings import settings
from pathlib import Path
from PIL import Image

logger = settings.get_logger(__name__)


async def check_wordle_gues_for_noun(word: str, use_db: bool = True) -> bool:
    """
    Проверка, является ли слово существительным.
    :param word: Слово для проверки
    :type word: str
    :return: True если слово является существительным, иначе False
    :rtype: bool
    {"head":{},
    "def":
        [{"text":"время","pos":"noun","tr":
            [{"text":"момент","pos":"noun","fr":1,"syn":... ""
    """

    if use_db:
        result = await check_word_in_db(word)
        return result
    API_KEY = settings.YANDEX_DICT_API_KEY
    url = f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={API_KEY}&lang=ru-ru&text={word}"
    response = await requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'def' in data:
            for definition in data['def']:
                if definition.get('pos') == 'noun':
                    return True
    return False


def wordle_logic(guess: str, secret: str) -> List[int]:
    """
    Compares the guessed word with the secret word and returns a list of integers
    representing the result for each letter:
    2 - correct letter in the correct position (yellow)
    1 - correct letter in the wrong position (white)
    0 - incorrect letter (black)
    """
    result = [0] * len(guess)
    secret_temp: List[Optional[str]] = list(secret)
    logger.debug(f"Comparing guess: {guess} with secret: {secret}")
    # First pass: check for correct letters in correct positions
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            result[i] = 2
            secret_temp[i] = None  # Mark this letter as used

    # Second pass: check for correct letters in wrong positions
    for i in range(len(guess)):
        if result[i] == 0 and guess[i] in secret_temp:
            result[i] = 1
            # Mark this letter as used
            secret_temp[secret_temp.index(guess[i])] = None
    logger.debug(f"Result compare: {result}")

    return result


async def generate_wordle_image(user_id: int, guess: str, secret: str, attempt: int = 0) -> Path:
    """
    Generates a Wordle-style image for the given word.
    """

    if not attempt:
        bg = Image.open(settings.BASE_STATIC_PATH / "bg.png")
    else:
        bg = Image.open(settings.BASE_MEDIA_PATH / f"{user_id}_wordle.png")
    file_mask = wordle_logic(guess, secret)
    colors = {0: 'black', 1: 'white', 2: 'yellow'}
    image_path = [
        settings.BASE_STATIC_PATH / f"{char.upper()}_{colors[i]}.png" for char, i in zip(guess, file_mask)]

    img = Image.open(image_path[0])

    for i in range(0, len(guess)):
        img = Image.open(image_path[i])
        bg.paste(img, (25 + i * 132, 25 + attempt * 132), img)
    path_file = settings.BASE_MEDIA_PATH / f"{user_id}_wordle.png"
    bg.save(path_file)
    return path_file
