#!/usr/bin/env python3
"""Единый сервер EasyPython: Mini App (FastAPI) + Telegram-бот (webhook).

На хостинге (Render) достаточно ОДНОГО сервиса:
  uvicorn server:app --host 0.0.0.0 --port $PORT

При старте сервер пробует зарегистрировать webhook у Telegram.
Если хост ещё не доступен (первый запуск), не роняет сервер —
webhook можно зарегистрировать повторно после того, как Render
выдаст最終ic HTTPS-адрес.
"""

import os
import logging

from dotenv import load_dotenv
load_dotenv()

from fastapi import Request
from fastapi.responses import JSONResponse

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Импортируем настоящее приложение со всеми маршрутами Mini App
from app.main import app

# --------------------------------------------------------------------------- #
# Конфигурация
# --------------------------------------------------------------------------- #
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "http://localhost:8000")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в переменных окружения")


# --------------------------------------------------------------------------- #
# Обработчики команд бота
# --------------------------------------------------------------------------- #
async def _cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие + кнопка открытия Mini App."""
    keyboard = [[InlineKeyboardButton(
        text="🐍 Открыть EasyPython",
        web_app=WebAppInfo(url=WEB_APP_URL),
    )]]
    await update.message.reply_text(
        "Привет! Я EasyPython — учитель Python в стиле Duolingo.\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение и начать учиться:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def _cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команды:\n/start — открыть приложение EasyPython\n/help — помощь"
    )


async def _error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Ошибка при обработке update", exc_info=context.error)


# --------------------------------------------------------------------------- #
# Telegram Application (webhook-режим, без polling)
# --------------------------------------------------------------------------- #
bot_app = Application.builder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("start", _cmd_start))
bot_app.add_handler(CommandHandler("help", _cmd_help))
bot_app.add_error_handler(_error_handler)


# --------------------------------------------------------------------------- #
# Регистрация webhook при старте, удаление при остановке
# --------------------------------------------------------------------------- #
@app.on_event("startup")
async def _on_startup():
    await bot_app.initialize()
    await bot_app.start()
    webhook_url = f"{WEB_APP_URL.rstrip('/')}/webhook/{BOT_TOKEN}"
    try:
        await bot_app.bot.set_webhook(webhook_url)
        logger.info(f"Telegram webhook установлен: {webhook_url}")
    except Exception as exc:
        # Не роняем сервер, если webhook не доступен ещё (первый запуск)
        logger.warning(f"Не удалось установить webhook (continuing): {exc}")


@app.on_event("shutdown")
async def _on_shutdown():
    try:
        await bot_app.bot.delete_webhook()
    except Exception as exc:
        logger.warning(f"Не удалось удалить webhook: {exc}")
    await bot_app.stop()
    await bot_app.shutdown()


# --------------------------------------------------------------------------- #
# Webhook endpoint: принимает update от Telegram
# --------------------------------------------------------------------------- #
@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != BOT_TOKEN:
        return JSONResponse({"error": "invalid token"}, status_code=403)
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return JSONResponse({"ok": True})


# --------------------------------------------------------------------------- #
# Точка входа для uvicorn (Procfile)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
