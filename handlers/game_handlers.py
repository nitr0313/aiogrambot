from aiogram import html, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.command import Command
from keyboards import keyboards as kb
from utils.wordle_utils import check_wordle_gues_for_noun
from states import WordGame

wordle = Router()
MAX_TRIES = 6


@wordle.message(Command("wordle_reset"))
async def help_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Сброс игры", reply_markup=kb.get_main_keyboard()
    )
    await state.clear()


@wordle.message(Command("wordle"))
async def wordle_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Игра пока в разработке, но можно попробовать отгадать единственное слово.",
        reply_markup=kb.get_wordle_keyboard())
    await state.clear()
    # random word choice
    await state.set_state(WordGame.next_letter)
    await state.update_data({
        "tries": 0,
        "word": "проба",  # This should be replaced with a random word selection
        "current_try": "",
        "guesses": []
    })


@wordle.message(WordGame.next_letter)
async def wordle_next_letter_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    print(f"SET LETTER {data=}")
    if message.text == "⬅":
        if len(data['current_try']) == 0:
            await message.answer(
                text="Нет букв для удаления.",
                reply_markup=kb.get_wordle_keyboard(data=await state.get_data())
            )
            return
        data['current_try'] = data['current_try'][:-1]
        await state.set_data(data)
        await message.answer(
            text="Буква удалена.",
            reply_markup=kb.get_wordle_keyboard(data=data)
        )
        return
    data['current_try'] += message.text[-1]
    await state.set_data(data)
    await message.answer(
        text=f"{message.text[-1]}", reply_markup=kb.get_wordle_keyboard(data=data))
    if len(data['current_try']) >= 5:
        await message.answer(
            text=f"Вы уже набрали 5 букв - отправляйте слово целиком нажатием ➡",
            reply_markup=kb.get_wordle_keyboard(data=data)
        )
        await state.set_state(WordGame.try_word)


@wordle.message(WordGame.try_word, F.text == "⬅")
async def wordle_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    print(f"Try word {data=}")
    if len(data['current_try']) == 0:
        await message.answer(
            text="Нет букв для удаления.",
            reply_markup=kb.get_wordle_keyboard(data=await state.get_data())
        )
    else:
        data['current_try'] = data['current_try'][:-1]
        await state.set_data(data)
        await message.answer(
            text="Буква удалена.",
            reply_markup=kb.get_wordle_keyboard(data=data)
        )
    await state.set_state(WordGame.next_letter)


@wordle.message(WordGame.try_word, F.text == "➡")
async def wordle_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    print(f"Try word {data=}")
    if len(data['current_try']) < 5:
        await message.answer(
            text="Еще не 5 букв - добери до слова из 5 букв",
            reply_markup=kb.get_wordle_keyboard(data=await state.get_data())
        )
        await state.set_state(WordGame.next_letter)
        return

    if not check_wordle_gues_for_noun(data['current_try']):
        await message.answer(
            text="Слово не является существительным. Попробуйте другое слово.",
            reply_markup=kb.get_wordle_keyboard(data=await state.get_data())
        )
        await state.set_state(WordGame.next_letter)
        return
    data["guesses"].append(data["current_try"])
    data["current_try"] = ""
    data["tries"] += 1

    if data["word"] == data["guesses"][-1]:
        await message.answer(
            text=f"Поздравляю! Вы угадали слово! {html.italic(data['word'])}🎉",
            reply_markup=kb.get_main_keyboard())
        # TODO Сохранить статистику в базу данных здесь
        await state.clear()

        return

    guess = message.text.strip().lower()
    if data["tries"] < MAX_TRIES:
        await message.answer(f"Не верно попробуйте снова. Осталось попыток: {MAX_TRIES - data['tries']}",
                             reply_markup=kb.get_wordle_keyboard(data=data))
        # Распечатать все попытки и буквы в цвета состояний
        await message.answer(
            text="Текущие попытки:\n" +
                 "\n".join([f"{idx + 1}. {html.bold(try_word)}"
                            for idx, try_word in enumerate(data['guesses'])]),
            reply_markup=kb.get_wordle_keyboard(data=data)
        )
        await state.set_data(data)
        await state.set_state(WordGame.next_letter)

    if data["tries"] >= MAX_TRIES:
        await message.answer(
            text=f"Конец игры! Правильное слово '{data['word']}'.",
            reply_markup=kb.get_main_keyboard())
        await state.clear()


@wordle.message(Command("game_help"))
async def help_handler(message: Message):
    await message.answer(
        text="📖 Правила игры Wordle: Угадайте 5-буквенное слово за 6 попыток. "
        "Вводите буквы с помощью клавиатуры и подтверждайте ответ кнопкой ➡. Удачи! 🍀"
    )
