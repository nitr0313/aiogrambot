from aiogram import html, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters.command import CommandStart, Command
from datetime import date
from db.dao import get_user, get_users, set_user
from keyboards import keyboards as kb
from settings import admins

from utils.utils import get_joke_by_id
from states import Reg

user = Router()

# while simple db :)
users_bd: dict = {}


@user.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user is not None:
        await message.answer(
            text=f"С возвращением, {html.bold(user.full_name)}!",
            reply_markup=kb.get_main_keyboard()
        )
        return
    await message.answer(
        text="".join([html.bold("Привет!"),
                      "Это простой бот на Aiogram.\n\nРегистрация:\n",
                      "Введите ваше имя"]),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Reg.waiting_for_name)


@user.message(Reg.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    user = await set_user(tg_id=message.from_user.id, username=message.from_user.username, full_name=user_data['name'])
    await message.answer(
        text=f"Регистрация завершена!\nВаше имя: {user_data['name']}\nДата регистрации: {date.today().strftime('%d.%m.%Y')}",
        reply_markup=kb.get_main_keyboard()
    )
    await state.clear()
    await state.set_state(Reg.waiting_for_age)


@user.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        text="To use this bot, simply send any message, and I will echo it back to you.\n"
             "Use /start to see the welcome message again."
    )


@user.message(Command("users"))
async def users_handler(message: Message):
    if message.from_user.id not in admins:
        await message.answer("No registered users.")
        return
    response = "Registered Users:\n"
    users = await get_users()
    for user in users:
        response += (f"ID: {user.id}, Name: {user.full_name} "
                     f"Registered on: {user.created_at}\n")
    await message.answer(response)


@user.message(Command("joke"))
async def joke_handler(message: Message):
    from utils.utils import get_new_joke
    joke = await get_new_joke()
    await message.answer(text=joke, reply_markup=kb.get_joke_keyboard())


@user.callback_query(F.data.startswith('joke_'))
async def joke_callback_handler(callback_query: CallbackQuery):
    if callback_query.data is None:
        return
    joke_id = int(callback_query.data.split('_')[1])
    await callback_query.answer(text=f"Вы выбрали шутку {joke_id}")

    if callback_query.message:
        await callback_query.message.answer(text=get_joke_by_id(joke_id))


@user.message(Command("myid"))
async def myid_handler(message: Message):
    if message.from_user is None:
        await message.answer("Не удалось получить ваш userID.")
        return
    await message.answer(text=f"Ваш userID: {message.from_user.id}", reply_markup=kb.get_main_keyboard())


@user.message(F.photo)
async def photo_id(message: Message):
    if not message.photo:
        await message.answer("Нет фото в сообщении.")
    await message.answer(text=f"Photo file_id: {message.photo[-1].file_id}")
    await message.answer_photo(photo=message.photo[0].file_id, text=f"Here is your {message.photo[0].file_id=}!")


# @user.message()
# async def echo_handler(message: Message):
#     await message.send_copy(chat_id=message.chat.id)
