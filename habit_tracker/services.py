import os
import requests
from config import settings
from dotenv import load_dotenv

load_dotenv()


def send_telegram_message(chat_id, text):
    """Отправляет сообщение в Telegram"""
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}

    response = requests.post(url, json=data)

    if response.status_code != 200:
        print(f"Ошибка отправки в Telegram: {response.text}")
