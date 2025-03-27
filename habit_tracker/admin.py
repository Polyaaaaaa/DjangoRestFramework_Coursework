from django.contrib import admin

from habit_tracker.models import Habit


# Register your models here.
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'time', 'action', 'is_pleasant', 'periodicity', 'reward', 'time_to_complete', 'is_public')
    list_filter = ('user', 'is_pleasant', 'is_public', 'periodicity')
    search_fields = ('action', 'place')
