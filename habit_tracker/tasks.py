from celery import shared_task
from django_celery_beat.utils import now
from habit_tracker.models import Habit
from habit_tracker.services import send_telegram_message


@shared_task
def send_habit_reminders():
    """Отправляет напоминания о привычках"""
    current_time = now().time()
    habits = Habit.objects.filter(time=current_time)

    for habit in habits:
        if habit.user and habit.user.tg_chat_id:
            message = f"🔔 Напоминание! {habit.action} в {habit.place}"
            send_telegram_message(habit.user.tg_chat_id, message)

    return f"Напоминания отправлены для {len(habits)} привычек"
