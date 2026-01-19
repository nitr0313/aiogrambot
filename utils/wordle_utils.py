import requests
# from config import YANDEX_DICT_API_KEY
from decouple import config
from db.dao import check_word_in_db


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
    API_KEY = config("YANDEX_DICT_API_KEY")
    url = f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={API_KEY}&lang=ru-ru&text={word}"
    response = await requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'def' in data:
            for definition in data['def']:
                if definition.get('pos') == 'noun':
                    return True
    return False


if __name__ == "__main__":
    test_words = ["время", "бежать", "красивый", "дом", "играть"]
    for word in test_words:
        is_noun = check_wordle_gues_for_noun(word)
        print(f"Слово '{word}' является существительным: {is_noun}")
