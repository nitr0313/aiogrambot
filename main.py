import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault

from create_bot import bot, dp
from settings import admins, logger
from db.base import create_tables, fill_tables
from handlers.handlers import user

from handlers.game_handlers import wordle


async def set_commands():
    commands = [BotCommand(command='start', description='Старт')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()
    await create_tables()
    # await fill_tables()

    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f'Я запущен🥳.')
        except:
            pass


# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass


async def main():
    dp.include_routers(wordle, user)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    exit(0)
