# Используем официальный Python
FROM python:3.11-slim

# Создаем рабочую директорию
WORKDIR /app

# Копируем только необходимые файлы
COPY requirements.txt .
COPY bot.py .
COPY config.py .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаем папку для логов при старте контейнера
RUN mkdir -p logs && touch logs/bot.log

# Точка входа: скрипт, который проверяет токен и запускает бота
ENTRYPOINT ["python", "bot.py"]
