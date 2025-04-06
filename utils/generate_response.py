import logging

from services import *
from . import *

logger = logging.getLogger("uvicorn")


async def generate_response(message: str, phone_number: str) -> str:
    logger.info("Parsing message")
    message = message.lower().strip()

    logger.info("Loading chat history")
    chat_history = await get_chat_history(phone_number)
    print(chat_history)

    logger.info("Loading all products")
    knowelage = await get_woocomerce_products()

    logger.info("Generating response")
    response = await ai_generate_response(message, chat_history, knowelage)

    return response
