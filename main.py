import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.handlers import user

from handlers.game_handlers import wordle


load_dotenv()
TELEBOT_TOKEN = getenv("TELEBOT_TOKEN")


async def main():
    bot = Bot(token=TELEBOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(wordle, user)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")
