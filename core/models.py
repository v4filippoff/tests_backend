from django.contrib.auth.models import User
from django.db import models


class Test(models.Model):
    """Модель теста"""
    name = models.CharField('test name', max_length=100)
    publish_date = models.DateField('publish date', auto_now_add=True)
    question_number = models.PositiveIntegerField('question number')
    is_deleted = models.BooleanField('is test deleted', default=False)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return f'Test (ID={self.id}): {self.name}'


class Question(models.Model):
    """Модель вопроса из теста"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('question text', max_length=400)

    def __str__(self):
        return f'Question: {self.text[:30]}'


class Answer(models.Model):
    """Модель варианта ответа на вопрос"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('question answer', max_length=200)
    is_correct = models.BooleanField('is answer correct')

    def __str__(self):
        return f'Answer: {self.text[:30]}'


class TestPassing(models.Model):
    """Модель прохождения теста пользователем"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passed_tests')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='passed_by_users')
    passing_date = models.DateField('passing date', auto_now_add=True)

    def __str__(self):
        return f'Test "{self.test.name}" passed by "{self.user.username}"'


class QuestionAnswer(models.Model):
    """Модель ответа на вопрос пользователем"""
    test_passing = models.ForeignKey(TestPassing, on_delete=models.CASCADE, related_name='question_answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answered_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answered_by_users')
    user_answer = models.BigIntegerField('user answer id')

    def __str__(self):
        return f'User "{self.user.username}" answered the question "{self.question.text[:30]}...": {self.user_answer}'