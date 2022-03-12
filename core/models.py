from django.db import models


class Test(models.Model):
    """Модель теста"""
    name = models.CharField('Название теста', max_length=200)
    publish_date = models.DateField('Дата публикации', auto_now_add=True)
    is_deleted = models.BooleanField('Тест удален', default=False)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return f'Тест (ID={self.id}): {self.name}'


class Question(models.Model):
    """Модель вопроса из теста"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Текст вопроса', max_length=400)

    def __str__(self):
        return f'Вопрос: {self.text[:30]}'


class Answer(models.Model):
    """Модель варианта ответа на вопрос"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Текст варианта ответа', max_length=200)
    is_correct = models.BooleanField('Правильный ответ')

    def __str__(self):
        return f'Вариант ответа: {self.text[:30]}'
