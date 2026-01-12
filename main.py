import asyncio
import logging
import sys

from create_bot import bot, dp
from handlers.handlers import user

from handlers.game_handlers import wordle


async def main():
    dp.include_routers(wordle, user)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")
