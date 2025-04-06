import logging

from services.mongodb_services import add_message, delete_phone_number_data, get_chat_history
from services.woocomerce_service import get_woocomerce_products
from services.llm_services import ai_generate_response

logger = logging.getLogger("uvicorn")


async def generate_response(message: str, phone_number: str) -> str:
    try:
        logger.info("Parsing message")
        message = message.lower().strip()

        if message.startswith("hello") or message.startswith("hi") or message.startswith("pozdrav"):
            await delete_phone_number_data(phone_number)

        logger.info("Loading chat history")
        chat_history = await get_chat_history(phone_number)
        print(chat_history)

        logger.info("Loading all products")
        knowledge = await get_woocomerce_products()

        logger.info("Generating response")
        response = await ai_generate_response(message, chat_history, knowledge)

        await add_message(phone_number, "user", message)
        await add_message(phone_number, "assistant", response)

        return response

    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        return "Ups, imamo mali problem. Pokušaj ponovo poslati istu poruku"
