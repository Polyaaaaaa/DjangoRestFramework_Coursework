from django.urls import path

from habit_tracker.views import UserHabitListView, PublicHabitListView, HabitCreateView, HabitDetailView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

app_name = 'habit_tracker'

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("api/my-habits/", UserHabitListView.as_view(), name="user-habits"),
    path("api/public-habits/", PublicHabitListView.as_view(), name="public-habits"),
    path("api/habits/create/", HabitCreateView.as_view(), name="create-habit"),
    path("api/habits/<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
