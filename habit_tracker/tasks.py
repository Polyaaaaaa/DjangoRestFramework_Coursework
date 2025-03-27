from celery import shared_task
from django_celery_beat.utils import now

from habit_tracker import bot
from habit_tracker.models import Habit


@shared_task
def send_habit_reminders():
    """Отправляет напоминания пользователям о привычках"""
    current_time = now().time()
    habits = Habit.objects.filter(time=current_time)

    for habit in habits:
        if habit.user.tg_chat_id:
            message = f"🔔 Напоминание! {habit.action} в {habit.place}"
            bot.send_telegram_message(chat_id=habit.user.tg_chat_id, text=message)

    return f"Напоминания отправлены для {len(habits)} привычек"