from django.core.exceptions import ValidationError


class TimeToCompleteValidator:
    """Проверяет, что время выполнения не превышает 120 секунд."""

    def __call__(self, value):
        if value > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")


class PeriodicityValidator:
    """Проверяет, что периодичность не превышает 7 дней."""

    def __call__(self, value):
        if value > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")


class HabitConstraintsValidator:
    """Дополнительные проверки модели Habit."""

    def __call__(self, habit):
        # Исключаем одновременное заполнение `reward` и `associated_habit`
        if habit.reward and habit.associated_habit:
            raise ValidationError("Можно заполнить только одно поле: либо 'вознаграждение', либо 'связанная привычка'.")

        # Проверяем, что связанная привычка является приятной
        if habit.associated_habit and not habit.associated_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if habit.is_pleasant and (habit.reward or habit.associated_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")
