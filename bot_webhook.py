#!/usr/bin/env python3
"""Telegram-бот EasyPython в режиме webhook.

Модуль самодостаточный: его можно подключить к любому FastAPI-приложению
через mount(app). Это сделано намеренно — на Render стартовая команда
может быть указана как `uvicorn app.main:app`, и тогда routes из server.py
не попадают в приложение. Подключение из app/main.py гарантирует, что
маршрут /webhook/{token} существует при любом варианте запуска.
"""

import os
import logging

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "http://localhost:8000").rstrip("/")

# Заполняется в _build_application()
bot_app = None


def _build_application():
    """Создаёт Telegram Application с обработчиками команд (ленивая сборка)."""
    global bot_app
    if bot_app is not None:
        return bot_app
    if not BOT_TOKEN:
        logger.warning("BOT_TOKEN не задан — бот в webhook-режиме отключён")
        return None

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
    from telegram.ext import Application, CommandHandler

    async def cmd_start(update, context):
        """Приветствие + кнопка открытия Mini App."""
        keyboard = [[InlineKeyboardButton(
            text="🐍 Открыть EasyPython",
            web_app=WebAppInfo(url=WEB_APP_URL),
        )]]
        await update.message.reply_text(
            "Привет! Я EasyPython — учитель Python в стиле Duolingo.\n\n"
            "Нажми кнопку ниже, чтобы открыть приложение и начать учиться:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def cmd_help(update, context):
        await update.message.reply_text(
            "Команды:\n"
            "/start — открыть приложение EasyPython\n"
            "/help — помощь"
        )

    async def on_error(update, context):
        logger.error("Ошибка при обработке update", exc_info=context.error)

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_error_handler(on_error)
    bot_app = app
    return bot_app


def mount(app):
    """Подключает webhook-маршрут и хуки старта/остановки к FastAPI-приложению."""
    from fastapi import Request
    from fastapi.responses import JSONResponse

    bot = _build_application()

    if bot is not None:
        from telegram import Update

        @app.on_event("startup")
        async def _bot_startup():
            try:
                await bot.initialize()
                await bot.start()
                url = f"{WEB_APP_URL}/webhook/{BOT_TOKEN}"
                await bot.bot.set_webhook(url, drop_pending_updates=False)
                logger.info("Telegram webhook установлен: %s", url)
            except Exception as exc:  # не роняем сервер из-за webhook
                logger.warning("Не удалось установить webhook: %s", exc)

        @app.on_event("shutdown")
        async def _bot_shutdown():
            try:
                await bot.stop()
                await bot.shutdown()
            except Exception as exc:
                logger.warning("Ошибка при остановке бота: %s", exc)

        @app.post("/webhook/{token}")
        async def webhook(token: str, request: Request):
            """Принимает update от Telegram."""
            if token != BOT_TOKEN:
                return JSONResponse({"error": "invalid token"}, status_code=403)
            try:
                data = await request.json()
                await bot.process_update(Update.de_json(data, bot.bot))
                return JSONResponse({"ok": True})
            except Exception as exc:
                logger.exception("Сбой обработки update: %s", exc)
                return JSONResponse({"ok": False}, status_code=200)

    @app.get("/webhook-info")
    async def webhook_info():
        """Диагностика: что Telegram знает про webhook."""
        if bot is None:
            return {"configured": False, "reason": "BOT_TOKEN не задан"}
        try:
            info = await bot.bot.get_webhook_info()
            return {
                "configured": True,
                "url": info.url,
                "pending_update_count": info.pending_update_count,
                "last_error_message": info.last_error_message,
                "last_error_date": str(info.last_error_date),
                "expected_url": f"{WEB_APP_URL}/webhook/{BOT_TOKEN}",
            }
        except Exception as exc:
            return {"configured": True, "error": str(exc)}

    return bot
