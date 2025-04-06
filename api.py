import logging
import os
import json
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# TODO: Ovo nam ovdje ne treba
from services.mongodb_services import add_message, delete_phone_number_data, get_chat_history
from services.telegram_service import handle_telegram_message
from services.woocomerce_service import get_woocomerce_products
from utils import generate_response, process_message

app = FastAPI()
logger = logging.getLogger("uvicorn")
application = None


@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

    logger.info(
        f"Verify webhook: mode={mode}, token={token}, challenge={challenge}")
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return Response(content=challenge, media_type="text/plain")
        else:
            return Response(content="Forbidden", status_code=403)
    return Response(content="Not Found", status_code=404)


@app.post("/webhook")
async def webhook(request: Request):
    body_bytes = await request.body()
    body = json.loads(body_bytes)

    logger.info(f"Received webhook event: {body}")
    if body.get("object") == "whatsapp_business_account":
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value.get("messages", []):
                            await process_message(message)
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    global application
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables")
        raise ValueError("TELEGRAM_BOT_TOKEN is required")

    # Initialize Telegram bot
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_telegram_message))

    # Start the Telegram bot polling in the background
    async def start_polling():
        await application.initialize()
        await application.start()
        logger.info("Telegram bot started polling")

    # Run polling in background
    asyncio.create_task(start_polling())


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """Handle Telegram webhook updates."""
    if application is None:
        return {"error": "Telegram bot not initialized"}

    body = await request.json()
    update = Update.de_json(body, application.bot)
    await application.process_update(update)
    return {"status": "ok"}


@app.get("/delete")
async def delete():
    await delete_phone_number_data("+38763534038")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


def start_api():
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
