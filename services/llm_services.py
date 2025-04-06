import json
import os
from typing import Dict, Any, Optional
from openai import AsyncOpenAI

from utils.system_message import generate_system_message


async def ai_generate_response(prompt: str, chat_history: list[dict[str, Any]], knowledge_base: str) -> str:
    API_KEY = os.getenv("LLM_PROVIDER_KEY")
    BASE_URL = os.getenv("BASE_URL", "https://api.openai.com/v1")
    MODEL = os.getenv("MODEL", "gpt-3.5-turbo")

    system_prompt = generate_system_message(knowledge_base)
    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)

    response = await client.chat.completions.create(  # type: ignore
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *chat_history,
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1
    )

    return response.choices[0].message.content  # type: ignore
