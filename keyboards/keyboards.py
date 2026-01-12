from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from utils import get_today_jokes


def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start"), KeyboardButton(text="/help")],
            [KeyboardButton(text="/joke"), KeyboardButton(text="/myid")],
            [KeyboardButton(text="/wordle")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите команду",
    )
    return keyboard


def get_joke_keyboard():
    jokes = get_today_jokes()
    if not jokes:
        return None
    buttons = [[InlineKeyboardButton(
        text=f"{i}) {joke[:5]}...", callback_data=f"joke_{i}")] for i, joke in enumerate(jokes)]
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            *buttons
        ]
    )
    return inline_kb


def get_wordle_keyboard(data: dict | None = None):
    print(f"{data=}")

    current_try: str = "_____"
    add_enter = False
    if data is not None and "current_try" in data:
        current_try = data['current_try']
        if len(current_try) < 5:
            current_try += "_" * (5 - len(current_try))
        else:
            current_try = current_try[:5]
            add_enter = True
    current_try_kb = [KeyboardButton(text=char) for char in current_try]
    if add_enter:
        current_try_kb += [KeyboardButton(text="➡")]
    first_line_letters = "йцукенгшщзхъ"
    second_line_letters = "фывапролджэ"
    third_line_letters = "ячсмитьбю"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [*current_try_kb],
            [*create_keyboard_line(first_line_letters, data)],
            [*create_keyboard_line(second_line_letters, data)],
            [*create_keyboard_line(third_line_letters, data)],
            # [KeyboardButton(text="⚪й"), KeyboardButton(text="⚪ц"),
            #  KeyboardButton(text="⚪у"), KeyboardButton(text="⚪к"),
            #  KeyboardButton(text="⚪е"), KeyboardButton(text="⚪н"),
            #  KeyboardButton(text="⚪г"), KeyboardButton(text="⚪ш"),
            #  KeyboardButton(text="⚪щ"), KeyboardButton(text="⚪з"),
            #  KeyboardButton(text="⚪х"), KeyboardButton(text="⚪ъ")],

            # [KeyboardButton(text="⚪ф"), KeyboardButton(text="⚪ы"),
            #  KeyboardButton(text="⚪в"), KeyboardButton(text="⚪а"),
            #  KeyboardButton(text="⚪п"), KeyboardButton(text="⚪р"),
            #  KeyboardButton(text="⚪о"), KeyboardButton(text="⚪л"),
            #  KeyboardButton(text="⚪д"), KeyboardButton(text="⚪ж"),
            #  KeyboardButton(text="⚪э")],

            # [KeyboardButton(text="⚪я"), KeyboardButton(text="⚪ч"),
            #  KeyboardButton(text="⚪с"), KeyboardButton(text="⚪м"),
            #  KeyboardButton(text="⚪и"), KeyboardButton(text="⚪т"),
            #  KeyboardButton(text="⚪ь"), KeyboardButton(text="⚪б"),
            #  KeyboardButton(text="⚪ю")],
            [KeyboardButton(text="/wordle_reset"), KeyboardButton(text="⬅")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Начать игру Wordle",
    )
    return keyboard


def create_keyboard_line(letters: str, data: dict) -> list:
    """
    Создание строки клавиатур для Wordle.
    data -> word -загаданное секретное слово
         -> guesses - попытки отгадать
    определить статус букв:
    - есть в загаданном слове стоит на месте
    - есть в загаданном слове стоит не на месте
    - нет в загаданном слове
    - статус не известен

    :param letters: список букв (по линим клавиатуры)
    :type letters: str
    :param data: state {word: str, guesses: list[str]}
    :type data: dict
    :return: Список кнопок буквы со статусом
    :rtype: list
    """
    letter_status = ['⚪', '🔵', '🟢', '🔴']
    secret_word = data['word'].split() if data and 'word' in data else ""
    guesses = data['guesses'] if data and 'guesses' in data else []
    status_dict = {}
    for guess in guesses:
        for i, char in enumerate(guess):
            if char in secret_word:
                if secret_word[i] == char:
                    status_dict[char] = letter_status[2]  # correct position
                else:
                    if status_dict.get(char) != letter_status[2]:
                        status_dict[char] = letter_status[1]  # wrong position
            else:
                if char not in status_dict:
                    status_dict[char] = letter_status[3]  # not in word

    line = [KeyboardButton(text=char) for char in letters]
    return line
