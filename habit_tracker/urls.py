from django.urls import path

from habit_tracker.views import UserHabitListView, PublicHabitListView, HabitCreateView, HabitDetailView

urlpatterns = [
    path("api/my-habits/", UserHabitListView.as_view(), name="user-habits"),
    path("api/public-habits/", PublicHabitListView.as_view(), name="public-habits"),
    path("api/habits/create/", HabitCreateView.as_view(), name="create-habit"),
    path("api/habits/<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    ]