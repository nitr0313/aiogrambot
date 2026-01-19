## Быстрые инструкции для AI-агента (GitHub Copilot)

Ниже — компактное руководство, которое помогает сразу приступить к работе с этим репозиторием.

- **Цель проекта**: Telegram-бот на Aiogram (v3 style) с простыми функциями: регистрация пользователей, ежедневные анекдоты и мини-игра Wordle.
- **Точка входа**: `main.py` — включает роутеры (`dp.include_routers(wordle, user)`), регистрирует `startup`/`shutdown` обработчики и запускает polling.
- **Создание бота / диспетчера**: `create_bot.py` экспортирует `bot` и `dp`. Хранилище FSM — `MemoryStorage()`.

Архитектура и основные модули
- `handlers/` — все маршруты: `handlers.py` (user flows), `game_handlers.py` (wordle). Каждый набор — `Router` (aiogram.v3). При добавлении нового набора: создать `Router`, декорировать обработчики через `@router.message(...)`/`@router.callback_query(...)`, и подключить в `main.py`.
- `keyboards/keyboards.py` — фабрики клавиатур: `get_main_keyboard()`, `get_wordle_keyboard(data)`. UI-логика (статусы клавиш Wordle) реализована в `create_keyboard_line`.
- `db/` — асинхронные SQLAlchemy модели и утилиты:
  - `database.py` — создает `engine = create_async_engine('sqlite+aiosqlite:///db.sqlite3')` и `async_session`.
  - `base.py` — `connection` декоратор используется для автоматического создания сессии в DAO.
  - `models.py` — `User`, `WordleStats`, `DailyJokes`.
  - `dao.py` — примеры использования: `@connection async def get_user(session, tg_id): ...`.
- `utils/` — вспомогательные функции:
  - `utils.py` — логика получения анекдотов (`get_new_joke`) использует `requests` + парсер `utils/parse_jokes.py` и кеширует/сохраняет через `db.dao`.
  - `wordle_utils.py` — проверка слова через Yandex Dictionary API; требует переменную окружения `YANDEX_DICT_API_KEY`.

Важные проектные конвенции
- Конфигурация через `python-decouple`: `settings.py` ожидает `TELEBOT_TOKEN` и `ADMINS` (список разделённых запятыми id). Пример `.env`:

```
TELEBOT_TOKEN=123:ABC
ADMINS=11111111,22222222
YANDEX_DICT_API_KEY=your_key_here
```

- DB: нет миграций — таблицы создаются вызовом `create_tables()` в `main.start_bot()` (см. `db/base.create_tables`).
- Асинхронность: все DB-операции — async/await. Следуйте async-паттерну в новых DAO и handler'ах.
- Обработчики используют aiogram.v3: `Router`, декораторы `@router.message(...)`, фильтры `F`, FSM — states в `states.py`.

Как запускать / отлаживать
- Локально (PowerShell):
  - Установить env vars (или `.env`) и запустить:

```powershell
$env:TELEBOT_TOKEN="<token>"; $env:ADMINS="111,222"; python .\main.py
```

- Через Docker Compose:

```powershell
docker-compose up --build
```

- При старте `main.py` вызывает `create_tables()` и отправляет сообщение администраторам (если указаны `ADMINS`).

Критические интеграции и внешние зависимости
- Aiogram v3 (Router/Dispatcher API). См. `create_bot.py` и `main.py`.
- SQLAlchemy Async + `aiosqlite`. DB URL в `db/database.py`.
- Yandex Dictionary API (опционально) — `utils/wordle_utils.py` использует `YANDEX_DICT_API_KEY`.
- RSS анекдотов: `https://www.anekdot.ru/rss/export_j.xml` парсится `utils/parse_jokes.py`.

Примеры типичных задач и примечания
- Добавить новый handler: создать `Router`, декорировать, импортировать и подключить в `main.py`.
  - Пример: в `handlers/game_handlers.py` есть `wordle = Router()` и `@wordle.message(Command("wordle"))`.
- Добавить DB-метод: использовать `@connection` из `db/base.py` и типизацию как в `db/dao.py`.
- Работа со State: обработчики используют FSMContext и состояния в `states.py`; при изменении состояний — всегда `await state.set_state(...)` и `await state.set_data(...)`.

Что не искать здесь
- В проекте нет тестовой инфраструктуры и миграций — не ожидайте pytest/alembic конфигов.

Чеклист PR кода (коротко)
- Новые роутеры экспортируются и подключаются в `main.py`.
- Асинхронные DB-вызовы обёрнуты в `@connection`.
- Новые env-vars документируются в README и `.env.example` (если добавлены).

Если что-то неясно — укажите, какую часть кода хотите расширить или где нужны примеры (например: добавить новый handler, написать DB-метод, интегрировать внешний API). 

---
Пожалуйста, сообщите, нужна ли детализация по: запуску в контейнере, шаблонам новых роутеров, оформлению сообщений администраторам или примерах SQLAlchemy async-запросов.
