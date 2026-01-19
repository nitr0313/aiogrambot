from sqlalchemy import BigInteger, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base


# Модель для таблицы пользователей
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    # Связи с заметками и напоминаниями
    wordle_stats: Mapped[list["WordleStats"]] = relationship(
        "WordleStats", back_populates="user", cascade="all, delete-orphan")


class WordleWord(Base):
    __tablename__ = 'wordle_words'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


# Модель для таблицы статистики Wordle
class WordleStats(Base):
    __tablename__ = 'wordle_stats'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    word: Mapped[str] = mapped_column(String, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False)
    success: Mapped[bool] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="wordle_stats")


class DailyJokes(Base):
    __tablename__ = 'daily_jokes'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    jokes_dict: Mapped[str] = mapped_column(Text, nullable=False)

    date: Mapped[str] = mapped_column(String, nullable=False, unique=True)
