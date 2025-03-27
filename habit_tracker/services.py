import os

from celery.worker.state import requests

from config.settings import TELEGRAM_URL
from dotenv import load_dotenv


load_dotenv()


def send_telegram_message(chat_id, message):
    params = {
        'text': message,
        'chat_id': chat_id,
    }
    response = requests.get(f'{TELEGRAM_URL}{os.getenv("BOT_TOKEN")}/sendMessage', params=params)
