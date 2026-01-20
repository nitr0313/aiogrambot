import json
from .database import async_session, engine, Base


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def fill_tables():
    from .dao import fill_wordle_words
    from os import path
    file = path.join(path.abspath(path.dirname(__file__)),
                     'russian_nouns_with_definition.json')

    with open(file, 'r', encoding='utf-8') as f:
        wordle_words_dict = json.load(f)

    await fill_wordle_words(wordle_words_dict)
