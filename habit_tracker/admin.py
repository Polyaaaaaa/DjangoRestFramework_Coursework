from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Панель администратора Django
    path("habit_tracker/", include("habit_tracker.urls")),  # Пути из habit_tracker
    path("users/", include("users.urls")),  # Пути из users
]
