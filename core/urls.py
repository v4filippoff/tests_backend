from django.urls import path

from core.views import CreateUserView, TestListView, TestDetailView

urlpatterns = [
    path('users/', CreateUserView.as_view(), name='user-create'),

    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/<int:pk>', TestDetailView.as_view(), name='test-detail'),
]
