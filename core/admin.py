from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedTabularInline

from core.models import Test, Question, Answer, TestPassing, QuestionAnswer


class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 0
    min_num = 2


class QuestionInline(NestedTabularInline):
    model = Question
    extra = 0
    min_num = 1
    inlines = [AnswerInline]


class TestAdmin(NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'publish_date', 'question_number', 'is_deleted')
    list_filter = ('publish_date', 'is_deleted')
    list_per_page = 10


admin.site.register(Test, TestAdmin)

class TestPassingAdmin(admin.ModelAdmin):
    pass

class QuestionAnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(TestPassing, TestPassingAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
