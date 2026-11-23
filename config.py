"""Конфигурация бота EasyPython."""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "students.db")

# Настройки бота
PARSE_MODE = "HTML"
TIMEOUT = 30

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в .env файле")