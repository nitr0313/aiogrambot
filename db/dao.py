import json
from settings import logger
from .base import connection
from .models import User, WordleStats, DailyJokes
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError


@connection
async def set_user(session, tg_id: int, username: str, full_name: str) -> Optional[User]:
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
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))
        return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении пользователя: {e}")
    return None


@connection
async def get_users(session) -> List[User]:
    try:
        users = await session.scalars(select(User))
        return users.all()
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении пользователей: {e}")
    return None


@connection
async def set_daily_jokes(session, dt, jokes) -> Optional[User]:
    print(f"Set jokes for date:", dt, jokes)
    try:
        db_jokes = await session.scalar(select(DailyJokes).filter_by(date=dt))
        if not db_jokes:
            jokes_dict = json.dumps(jokes)
            print(f"{jokes_dict=}")
            db_jokes = DailyJokes(date=dt, jokes_dict=jokes_dict)
            print(f"{db_jokes}")
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
    try:
        jokes = await session.scalar(select(DailyJokes).filter_by(date=dt))
        if jokes:
            return json.loads(jokes.jokes_dict)
        return []
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении шуток: {e}")
    return []
