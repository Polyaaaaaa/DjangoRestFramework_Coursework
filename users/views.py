from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.serializers import UserRegisterSerializer


# Create your views here.
class RegisterView(CreateAPIView):
    """Регистрация нового пользователя"""
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]



