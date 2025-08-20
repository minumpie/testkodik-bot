from dotenv import load_dotenv
import os

# Пробуем загрузить из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Если не найден — запрашиваем у пользователя
if not BOT_TOKEN:
    BOT_TOKEN = input("Введите ваш Telegram BOT_TOKEN: ").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан!")
