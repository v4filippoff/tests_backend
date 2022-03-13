from rest_framework import serializers
from django.contrib.auth.models import User

from core.models import Test, Question, Answer, TestPassing, QuestionAnswer


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания (регистрации) пользователя"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


class TestSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения тестов"""
    class Meta:
        model = Test
        fields = (
            'id',
            'name',
            'publish_date',
            'question_number',
        )


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения варианта ответа"""
    class Meta:
        model = Answer
        fields = (
            'id',
            'text',
            'is_correct',
        )


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения вопроса из теста"""
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'answers',
        )


class TestDetailSerializer(TestSerializer):
    """Сериализатор для детального отображения теста"""
    questions = QuestionSerializer(many=True)

    class Meta(TestSerializer.Meta):
        fields = TestSerializer.Meta.fields + ('questions',)


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа на вопрос пользователем"""
    class Meta:
        model = QuestionAnswer
        fields = (
            'question',
            'user_answer',
        )


class TestPassingSerializer(serializers.Serializer):
    """Сериализатор для прохождения теста пользователем"""
    question_answers = QuestionAnswerSerializer(many=True)

    def create(self, validated_data):
        question_answers = validated_data.pop('question_answers')
        test_passing_object = TestPassing.objects.create(**validated_data)

        objs = [
            QuestionAnswer(
                test_passing=test_passing_object,
                user=validated_data['user'],
                question=aq['question'],
                user_answer=aq['user_answer']
            ) for aq in question_answers
        ]
        QuestionAnswer.objects.bulk_create(objs)

        return test_passing_object