from django.contrib import admin
from django.contrib.auth.models import User


class InputFilter(admin.SimpleListFilter):
    """Базовый класс для фильтрации на основе текстового поля"""
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return ((None, None),)


class UserFilter(InputFilter):
    """Фильтр для поиска тестов, пройденных определенным пользователем"""
    parameter_name = 'user'
    title = 'user'

    def queryset(self, request, queryset):
        if self.value() is not None:
            try:
                user = User.objects.filter(username=self.value()).get()
            except User.DoesNotExist:
                return queryset.none()

            passed_test_ids = user.testpassing_set.values_list('test_id', flat=True)
            return queryset.filter(id__in=passed_test_ids)

