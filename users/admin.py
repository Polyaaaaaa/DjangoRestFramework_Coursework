from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Определяем поля, которые будут отображаться в списке объектов
    list_display = (
    'email', 'username', 'first_name', 'last_name', 'phone_number', 'city', 'tg_chat_id', 'is_staff', 'is_active')

    # Добавляем возможность поиска по этим полям
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')

    # Добавляем фильтрацию по полям
    list_filter = ('is_active', 'is_staff')

    # Определяем, какие поля будут редактируемыми на форме
    fields = (
    'email', 'username', 'first_name', 'last_name', 'phone_number', 'city', 'avatar', 'tg_chat_id', 'password',
    'is_staff', 'is_active')
    readonly_fields = ('email',)
