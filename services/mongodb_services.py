from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any
import os

# Updated MongoDB Client to use motor for async


async def get_mongo_client() -> AsyncIOMotorClient:
    MONGO_USER = os.getenv("MONGO_USER", "mongo")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "mongo")
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", "27017")
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

    client = AsyncIOMotorClient(MONGO_URI)
    return client

# Ensure to await get_mongo_client() in async functions


async def get_chat_history(phone_number: str) -> list[dict[str, Any]]:
    DB_NAME = "chatbot"
    COLLECTION_NAME = "conversations"

    client = await get_mongo_client()  # Await the client initialization
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    doc = await collection.find_one({}, {f"chats.{phone_number}": 1, "_id": 0})
    return doc.get("chats", {}).get(phone_number, [])

# Ensure to await get_mongo_client() in async functions


async def add_message(phone_number: str, role: str, content: str):
    DB_NAME = "chatbot"
    COLLECTION_NAME = "conversations"

    client = await get_mongo_client()  # Await the client initialization
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    query = {f"chats.{phone_number}": {"$exists": True}}
    update = {
        "$push": {
            f"chats.{phone_number}": {
                "role": role,
                "content": content
            }
        }
    }

    result = await collection.update_one(query, update)

    if result.matched_count == 0:
        # First time chat for this phone number, create it
        await collection.update_one(
            {},  # assumes only one document
            {"$set": {f"chats.{phone_number}": [
                 {"role": role, "content": content}]}},
            upsert=True
        )


async def delete_phone_number_data(phone_number: str):
    DB_NAME = "chatbot"
    COLLECTION_NAME = "conversations"

    client = await get_mongo_client()  # Await the client initialization
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Delete the chat history for the specified phone number
    result = await collection.update_one(
        {},
        # Remove the phone number's data
        {"$unset": {f"chats.{phone_number}": ""}}
    )

    # Optionally check if data was deleted successfully
    if result.modified_count > 0:
        print(f"Data for phone number {phone_number} deleted successfully.")
    else:
        print(f"No data found for phone number {phone_number}.")
