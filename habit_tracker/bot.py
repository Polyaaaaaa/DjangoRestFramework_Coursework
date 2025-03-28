import os
import django
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from asgiref.sync import sync_to_async

# Настраиваем Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Загружаем переменные окружения
load_dotenv()

from users.models import User

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    try:
        chat_id = update.message.chat_id
        username = update.message.from_user.username or f"user_{chat_id}"

        # Находим или создаем пользователя
        user, _ = await sync_to_async(User.objects.get_or_create, thread_sensitive=True)(username=username)

        # Сохраняем chat_id в User
        user.tg_chat_id = chat_id
        await sync_to_async(user.save, thread_sensitive=True)()

        await update.message.reply_text("Вы подписаны на уведомления о привычках!")

    except Exception as e:
        print(f"Ошибка в команде /start: {e}")


def main():
    """Запуск Телеграм-бота"""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
