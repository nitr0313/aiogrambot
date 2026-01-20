import logging
from pathlib import Path
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс для хранения настроек бота."""
    DEBUG: bool = Field(
        default=False, description="Debuging status")

    ADMINS: list[int] = Field(
        default=[0], description="Admins list tg_ids")
    BASE_MEDIA_PATH: Path = Path("media/wordle/")
    BASE_STATIC_PATH: Path = Path("static/wordle/")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    TOKEN: str = Field(default="", description="TG Bot Tocke from @BotFather")
    YANDEX_DICT_API_KEY: str = Field(
        default="", description="TG Bot Tocke from https://yandex.ru/dev/dictionary/keys/get/?service=dict")
    LOGGING_LEVEL: int = Field(default=logging.INFO, description="")

    def get_logger(self, name=__name__):
        logging.basicConfig(level=self.LOGGING_LEVEL if not self.DEBUG else logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        return logging.getLogger(name)

# admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
# logger = logging.getLogger(__name__)


# token = config('TOKEN')
settings = Settings()
