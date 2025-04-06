import logging
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram import Update

from utils.generate_response import generate_response

logger = logging.getLogger("uvicorn")


async def start_telegram_bot(application: Application):
    await application.initialize()
    await application.start()
    logger.info("Telegram bot started")


async def send_telegram_message(chat_id: str, message_text: str, application: Application) -> bool:
    try:
        await application.bot.send_message(chat_id=chat_id, text=message_text)
        return True
    except Exception as e:
        print(f"Error sending Telegram message: {str(e)}")
        return False


async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.text:
        chat_id = str(message.chat_id)
        user_message = message.text

        response = await generate_response(user_message, chat_id)

        await context.bot.send_message(chat_id=chat_id, text=response)
