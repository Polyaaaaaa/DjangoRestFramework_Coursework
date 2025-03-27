from django.db import models
from django.utils import timezone

from users.models import User
from .validators import TimeToCompleteValidator, PeriodicityValidator, HabitConstraintsValidator


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits", null=True, blank=True)
    place = models.CharField(max_length=255, verbose_name="Место", default="Не указано")
    time = models.TimeField(verbose_name="Время", default=timezone.now)
    action = models.CharField(max_length=255, verbose_name="Действие", default="Новое действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_habits",
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveIntegerField(
        default=1, validators=[PeriodicityValidator], verbose_name="Периодичность (в днях)"
    )
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )
    time_to_complete = models.PositiveIntegerField(
        validators=[TimeToCompleteValidator],
        verbose_name="Время на выполнение (в секундах)",
        default=60
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def clean(self):
        """Запускает валидатор модели."""
        HabitConstraintsValidator()(self)

    def __str__(self):
        return f"{self.action} в {self.time} ({'Приятная' if self.is_pleasant else 'Полезная'})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["user", "time"]


# class TelegramUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     chat_id = models.CharField(max_length=50, unique=True)
