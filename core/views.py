from rest_framework.generics import CreateAPIView

from core.serializers import CreateUserSerializer


class CreateUserView(CreateAPIView):
    """Создает (регистрирует) нового пользователя"""
    serializer_class = CreateUserSerializer
