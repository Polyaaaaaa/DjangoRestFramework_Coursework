from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .models import Habit
from .pagination import HabitPagination
from .permissions import IsOwnerOrPublicReadOnly
from .serializers import HabitSerializer
from .services import send_telegram_message


class HabitListView(ListAPIView):
    """Выводит список привычек (с учетом доступа)"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Показываем пользователю его привычки + публичные"""
        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)
        return Habit.objects.filter(is_public=True)


class HabitDetailView(RetrieveUpdateDestroyAPIView):
    """Отдельная привычка (с учетом прав доступа)"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrPublicReadOnly]


class UserHabitListView(ListAPIView):
    """Список привычек текущего пользователя"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListView(ListAPIView):
    """Список публичных привычек"""
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitCreateView(CreateAPIView):
    """Создание новой привычки"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Привязываем привычку к текущему пользователю
        habit = serializer.save()
        habit.user = self.request.user
        habit = serializer.save()
        habit.save()
        print(habit)
        if habit.user.tg_chat_id:
            send_telegram_message(habit.user.tg_chat_id, "Создана новая привычка!")


class HabitDetailView(RetrieveUpdateDestroyAPIView):
    """Просмотр, редактирование, удаление привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrPublicReadOnly]
