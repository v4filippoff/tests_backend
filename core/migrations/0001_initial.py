# Generated by Django 3.2 on 2022-03-13 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='question answer')),
                ('is_correct', models.BooleanField(verbose_name='is answer correct')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=400, verbose_name='question text')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='test name')),
                ('publish_date', models.DateField(auto_now_add=True, verbose_name='publish date')),
                ('question_number', models.PositiveIntegerField(verbose_name='question number')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is test deleted')),
            ],
            options={
                'ordering': ['-publish_date'],
            },
        ),
        migrations.CreateModel(
            name='TestPassing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passing_date', models.DateField(auto_now_add=True, verbose_name='passing date')),
                ('correct_answers', models.PositiveIntegerField(verbose_name='correct answers')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.question')),
                ('test_passing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answers', to='core.testpassing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.answer')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='core.test'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core.question'),
        ),
    ]
