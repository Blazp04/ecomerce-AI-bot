from typing import Any, Dict, List
from fastapi import logger

from services import send_whatsapp_message
from utils import generate_response


async def process_message(message: Dict[str, Any]):
    message_id = message.get("id")
    from_number = message.get("from")
    message_type = message.get("type")

    logger.info(
        f"Processing message from  ({from_number}): Type={message_type}")

    if message_type == "text":
        text_body = message.get("text", {}).get("body", "")
        response_text = generate_response(text_body, from_number)
        await send_whatsapp_message(from_number, response_text)

    else:
        logger.info(f"Received unsupported message type: {message_type}")
        await send_whatsapp_message(from_number, f"I received your {message_type} message, but I can only process text messages at the moment.")
