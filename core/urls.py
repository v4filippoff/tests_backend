from django.urls import path

from core.views import CreateUserView

urlpatterns = [
    path('users/', CreateUserView.as_view(), name='users'),
]
