import requests
import random
from datetime import date
from db.dao import get_daily_jokes, set_daily_jokes
from utils.parse_jokes import parser


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
