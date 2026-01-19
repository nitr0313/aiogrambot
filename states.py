from aiogram.fsm.state import StatesGroup, State


class Reg(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()


class WordGame(StatesGroup):
    next_letter = State()
    try_word = State()
    win = State()  # - not used yet - for collect static


class GenImg(StatesGroup):
    waiting_for_description = State()
    generating = State()
