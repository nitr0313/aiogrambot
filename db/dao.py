from create_bot import logger
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
