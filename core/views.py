from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.serializers import CreateUserSerializer, TestSerializer, TestDetailSerializer, TestPassingSerializer
from core.models import Test, TestPassing


class CreateUserView(CreateAPIView):
    """Создает (регистрирует) нового пользователя"""
    serializer_class = CreateUserSerializer


class TestListView(ListAPIView):
    """Отображает список тестов"""
    queryset = Test.objects.filter(is_deleted=False)
    serializer_class = TestSerializer


class TestDetailView(RetrieveModelMixin, CreateModelMixin, GenericAPIView):
    """Отображает детализированно тест и обрабатывает прохождение теста пользователем"""
    queryset = Test.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not TestPassing.objects.filter(user=request.user, test=self.get_object()).exists():
            return self.create(request, *args, **kwargs)

        return Response({'detail': 'The user has already passed this test'}, status=status.HTTP_409_CONFLICT)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return TestDetailSerializer
        return TestPassingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, test=self.get_object())


