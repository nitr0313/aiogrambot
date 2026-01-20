from pathlib import Path
from typing import List, Optional
import requests
import random
from datetime import date
from db.dao import get_daily_jokes, set_daily_jokes
from utils.parse_jokes import parser
from html2image import Html2Image
from settings import logging
from PIL import Image


logger = logging.getLogger(__name__)

today_jokes: dict = {
}


async def get_new_joke() -> str:
    """
    Fetches a new joke from the RSS feed or returns a cached one for today.
    """
    dt_today = date.today().strftime("%d.%m.%Y")
    logger.info("Get joke for date:", dt_today)
    jokes = await get_daily_jokes(dt_today)
    if jokes:
        logger.info("Returning cached joke for today.")
        return random.choice(jokes)
    logger.info("Fetching new jokes from RSS feed.")
    resp = requests.get("https://www.anekdot.ru/rss/export_j.xml")
    xml_data = resp.content
    jokes = parser(xml_data)
    if not jokes:
        return "No jokes found."
    today_jokes[dt_today] = jokes
    jokes = await set_daily_jokes(dt_today, jokes)
    joke = random.choice(jokes)
    return joke


def get_today_jokes() -> list:
    """
    Returns the list of jokes for today.
    """
    dt_today = date.today().strftime("%d.%m.%Y")
    if jokes := today_jokes.get(dt_today):
        logger.info("Returning cached jokes for today.")
        return jokes
    logger.info("Fetching jokes for today from the database.")
    jokes = get_daily_jokes(dt_today)
    return today_jokes.get(dt_today, [])


def get_joke_by_id(id_: int | None) -> str:
    """
    Returns a cached joke by its ID for today.
    """
    jokes = get_today_jokes()
    if not jokes:
        return "No jokes found for today."
    if id_ is None:
        return random.choice(jokes)
    if 0 <= id_ < len(jokes):
        return jokes[id_]
    return "Joke not found."


async def create_img(message: str):
    ...  # Implementation for image creation goes here
    hti = Html2Image(size=(295, 150))

    html_str = ''.join(
        [f'<span class="let_{i}">{letter.capitalize()}</span>' for i, letter in enumerate(message)])
    path = hti.screenshot(
        html_str=f"<html><body><h1>{html_str}</h1></body></html>",
        css_str=["span { font-size: 48px; height: 40px; width: 40px; margin: 5px; border: 2px solid black; padding: 1px 5px 1px 5px; }",
                 "body { background: darkgray; }",
                 ".let_0 { color: white; background: gray; }",
                 ".let_1 { color: black; background: yellow; }",
                 ".let_2 { color: black; background: white; }",
                 ".let_3 { color: white;  background: gray; }",
                 ".let_4 { color: black; background: white; }"],
        save_as="generated_image.png"
    )
    return path


def wordle_logic(guess: str, secret: str) -> list[int]:
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
    BASE_MEDIA_PATH = Path("media/wordle/")  # TODO move to settings
    BASE_STATIC_PATH = Path("static/wordle/")
    if not attempt:
        bg = Image.open(BASE_STATIC_PATH / "bg.png")
    else:
        bg = Image.open(BASE_MEDIA_PATH / f"{user_id}_wordle.png")
    file_mask = wordle_logic(guess, secret)
    colors = {0: 'black', 1: 'white', 2: 'yellow'}
    image_path = [
        BASE_STATIC_PATH / f"{char.upper()}_{colors[i]}.png" for char, i in zip(guess, file_mask)]

    img = Image.open(image_path[0])

    for i in range(0, len(guess)):
        img = Image.open(image_path[i])
        bg.paste(img, (25 + i * 132, 25 + attempt * 132), img)
    path_file = BASE_MEDIA_PATH / f"{user_id}_wordle.png"
    bg.save(path_file)
    return path_file
