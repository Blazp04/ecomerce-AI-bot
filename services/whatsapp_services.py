
import os
import requests


async def send_whatsapp_message(to_number: str, message_text: str) -> dict:

    PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
    WHATSAPP_API_URL = f'https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages'
    ACCES_TOKEN = os.getenv('ACCES_TOKEN')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCES_TOKEN}"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    try:
        response = requests.post(
            WHATSAPP_API_URL, headers=headers, json=payload)
        print(f"Message sent to {to_number}, Response: {response.status_code}")
        print(response.text)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return None
