#!/usr/bin/env python3
"""Telegram bot for EasyPython Mini App - Web App integration"""

import os
import logging
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

WEB_APP_URL = os.getenv('WEB_APP_URL', 'http://localhost:8000')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - show button to open Mini App"""
    keyboard = [
        [InlineKeyboardButton(
            text="🐍 Открыть EasyPython",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Привет! Я EasyPython — учитель Python в стиле Duolingo.\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение и начать учиться:",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "Команды:\n/start — открыть приложение EasyPython\n/help — помощь"
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a message to user"""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    # Send error message to the user who triggered the error
    if update and update.message:
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")
    else:
        logger.error("Update has no message - cannot send error message")


async def main():
    """Start the bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_error_handler(error_handler)
    
    # Start the bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    logger.info("Bot is running. Press Ctrl+C to stop.")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
