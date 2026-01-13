FROM python:3.13-slim

# Установка рабочей директории
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY pyproject.toml .

# Установка зависимостей Python
RUN pip install --no-cache-dir -e .

# Копируем весь код проекта
COPY . .

# Создаем директорию для базы данных
RUN mkdir -p /app/data

# Запуск бота
CMD ["python", "main.py"]