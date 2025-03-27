# from telegram import Update
# from telegram.ext import CommandHandler, CallbackContext, Updater
# from django.core.wsgi import get_wsgi_application
# import os
# import django
# from .models import TelegramUser
# from django.contrib.auth.models import User
# from dotenv import load_dotenv
#
#
# # Настраиваем Django, если запускаем вне Django-контекста
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# django.setup()
#
# load_dotenv()
#
# TOKEN = os.getenv("BOT_TOKEN")
#
#
# def start(update: Update, context: CallbackContext):
#     try:
#         chat_id = update.message.chat_id
#         username = update.message.from_user.username or f"user_{chat_id}"
#
#         # Ищем пользователя по Telegram username или создаем нового
#         user, _ = User.objects.get_or_create(username=username)
#         TelegramUser.objects.get_or_create(user=user, chat_id=chat_id)
#
#         update.message.reply_text("Вы подписаны на уведомления о привычках!")
#     except Exception as e:
#         print(f"Error processing /start command: {e}")
#
#
# def main():
#     updater = Updater(TOKEN, use_context=True)
#     dp = updater.dispatcher
#     dp.add_handler(CommandHandler("start", start))
#
#     updater.start_polling()
#     updater.idle()
#
#
# if __name__ == "__main__":
#     main()
