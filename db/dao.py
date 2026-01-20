import json
from settings import logger
from .base import connection
from .models import User, WordleStats, DailyJokes, WordleWord
from sqlalchemy import func, select
from typing import List, Dict, Any, Optional, Union
from sqlalchemy.exc import SQLAlchemyError


@connection
async def set_user(session, tg_id: int, username: str, full_name: str) -> Optional[User]:
    """
    Добавляет нового пользователя в БД или обновляет существующего.
    :param session: Сессия SQLAlchemy
    :param tg_id: ID пользователя в Telegram
    :param username: Имя пользователя
    :param full_name: Полное имя пользователя
    :return: Пользователь или None, если не удалось добавить
    :rtype: User | None
    """
    logger.info(f"Пытаюсь добавить пользователя с ID {tg_id} в БД...")
    if not tg_id or not username or not full_name:
        logger.error(
            "Необходимо указать tg_id, username и full_name для добавления пользователя.")
        return None
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))
        if not user:
            new_user = User(id=tg_id, username=username, full_name=full_name)
            session.add(new_user)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()
    return None


@connection
async def get_user(session, tg_id: int) -> Optional[User]:
    """
    Получает пользователя по его ID из БД.
    :param session: Сессия SQLAlchemy
    :param tg_id: ID пользователя
    :return: Пользователь или None, если не найден
    :rtype: User | None
    """
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))
        return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении пользователя: {e}")
    return None


@connection
async def get_users(session) -> Optional[List[User]]:
    """
    Получает список всех пользователей из БД.
    :param session: Сессия SQLAlchemy
    :return: Список пользователей или None в случае ошибки
    :rtype: List[User] | None
    """
    try:
        users = await session.scalars(select(User))
        return users.all()
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении пользователей: {e}")
    return None


@connection
async def set_daily_jokes(session, dt: str, jokes: List[str]) -> Optional[List[str]]:
    """
    Сохраняет шутки в БД для указанной даты.

    :param session: Сессия SQLAlchemy
    :param dt: Дата в формате строки, например "01.01.2023"
    :param jokes: Список шуток для сохранения
    :return: Описание
    :rtype: List[str] | None
    """
    try:
        db_jokes = await session.scalar(select(DailyJokes).filter_by(date=dt))
        if not db_jokes:
            jokes_dict = json.dumps(jokes)
            db_jokes = DailyJokes(date=dt, jokes_dict=jokes_dict)
            session.add(db_jokes)
            await session.commit()
            logger.info(f"Сохранили шутки за текущий день {dt}!")
            return jokes
        else:
            logger.info(f"шутки за {dt} найдены!")
            return json.loads(db_jokes.jokes_dict)
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при шуток в БД: {e}")
        await session.rollback()
    return None


@connection
async def get_daily_jokes(session, dt) -> Optional[List[str]]:
    """ Получает шутки из БД для указанной даты.
    :param session: Сессия SQLAlchemy
    :param dt: Дата в формате строки, например "01.01.2023"
    :return: Список шуток или пустой список, если шутки не найдены
    :rtype: List[str] | None
    """
    try:
        jokes = await session.scalar(select(DailyJokes).filter_by(date=dt))
        if jokes:
            return json.loads(jokes.jokes_dict)
        return []
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении шуток: {e}")
    return []


@connection
async def fill_wordle_words(session, words: Dict[str, Dict[str, str]]):
    """
    fill_wordle_words - Заполняет таблицу WordleWord словами из переданного словаря.

    :param session: SQLAlchemy сессия
    :param words: Словарь слов и их описаний
    :type words: Dict[str, Dict[str, str]]
    """
    db_words: set = {w_word for w_word in await session.scalars(select(WordleWord))}
    try:
        for word, description in words.items():
            desc = description.get('definition', '')
            # Start Filter only 5-letter nouns, excluding plural and archaic forms
            if len(word) != 5:
                continue
            if 'мн.' in desc or 'устар.' in desc:
                continue
            # existing_word = await session.scalar(select(WordleWord).filter_by(word=word))
            if word in db_words:
                continue
            # End Filters
            new_word = WordleWord(
                word=word, description=desc)
            session.add(new_word)
        await session.commit()
        logger.info("Заполнили таблицу слов Wordle!")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при заполнении слов Wordle: {e}")
        await session.rollback()


@connection
async def get_random_wordle_word(session) -> Optional[WordleWord]:
    try:
        word = await session.scalar(
            select(WordleWord).order_by(func.random()).limit(1)
        )
        return word
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении случайного слова Wordle: {e}")
    return None


@connection
async def check_word_in_db(session, word: str) -> bool:
    try:
        existing_word = await session.scalar(
            select(WordleWord).filter(func.lower(
                WordleWord.word) == word.lower())
        )
        return existing_word is not None
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при проверке слова в БД: {e}")
    return False


@connection
async def add_wordle_stats(session, user_id: int, data: Dict[str, Union[str, List]]) -> None:
    logger.info(
        f"Пытаюсь добавить статистику пользователя {user_id=} по игре wordle в БД")
    try:
        wordle_stat = WordleStats(
            user_id=user_id, word=data['secret'], attempts=data['tries'], success=data['success'])
        session.add(wordle_stat)
        await session.commit()
        logger.info(
            f"Добавлена статистика пользваотеля с ID {user_id} по игре wordle!")
        return None
    except SQLAlchemyError as e:
        logger.error(
            f"Ошибка при добавлении статистики {user_id=} {data=}: {e}")
        await session.rollback()
    return None


@connection
async def get_wordle_stats(session, user_id) -> Optional[List[WordleStats]]:
    logger.info(
        f"Получение статистики по игре wordle для пользователя {user_id=}")
    try:
        games = await session.scalar(select(DailyJokes).filter_by(user_id=user_id))
        if games:
            return games
        return []
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении статистики {user_id=}: {e}")
        await session.rollback()
    return None
