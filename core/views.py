from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from core.serializers import CreateUserSerializer, TestSerializer, TestDetailSerializer, TestPassingSerializer, \
    PassedTestSerializer, PassedTestDetailSerializer
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
        test = self.get_object()
        user_answer_ids = [qa['user_answer'].id for qa in serializer.validated_data['question_answers']]

        correct_answers = 0
        for question in test.questions.prefetch_related('answers'):
            correct_answers += question.answers.filter(is_correct=True, id__in=user_answer_ids).exists()

        serializer.save(user=self.request.user, test=test, correct_answers=correct_answers)


class PassedTestListView(ListAPIView):
    """Отображает пройденные пользователем тесты"""
    serializer_class = PassedTestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.testpassing_set.all()


class PassedTestDetailView(RetrieveAPIView):
    """Отображает пройденный тест с пометками правильный или нет ответ"""
    serializer_class = PassedTestDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        test_pk = self.kwargs['pk']
        return get_object_or_404(TestPassing, user=self.request.user, test_id=test_pk)
