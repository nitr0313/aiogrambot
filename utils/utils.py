import requests
import random
from datetime import date
from db.dao import get_daily_jokes, set_daily_jokes
from utils.parse_jokes import parser
from html2image import Html2Image
from settings import logger
from PIL import Image

today_jokes: dict = {
}


async def get_new_joke() -> str:
    """
    Fetches a new joke from the RSS feed or returns a cached one for today.
    """
    dt_today = date.today().strftime("%d.%m.%Y")
    print("Get joke for date:", dt_today)
    jokes = await get_daily_jokes(dt_today)
    if jokes:
        print("Returning cached joke for today.")
        return random.choice(jokes)
    print("Fetching new jokes from RSS feed.")
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
    print(html_str)
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


async def generate_wordle_image(user_id: int, word: str, attempt: int = 0) -> Image.Image:
    """
    Generates a Wordle-style image for the given word.
    """
    BASE_MEDIA_PATH = "media/wordle/"
    BASE_STATIC_PATH = "static/wordle/"
    if not attempt:
        bg = Image.open(f"{BASE_STATIC_PATH}bg.png")
    else:
        bg = Image.open(f"{BASE_MEDIA_PATH}{user_id}_wordle.png")
    image_path = [
        f"{BASE_STATIC_PATH}{char.upper()}_yellow.png" for char in word]
    # get files from static folder
    # for char in word:
    #     if not char.isalpha():
    #         raise ValueError("Word must contain only alphabetic characters.")
    img = Image.open(image_path[0])

    for i in range(0, len(word)):
        img = Image.open(image_path[i])
        bg.paste(img, (5 + i * 140, 24 + attempt * 145), img)
    path_file = f"{BASE_MEDIA_PATH}{user_id}_wordle.png"
    bg.save(path_file)
    return path_file
