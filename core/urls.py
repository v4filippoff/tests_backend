from django.urls import path

from core.views import CreateUserView, TestListView, TestDetailView, PassedTestListView, PassedTestDetailView

urlpatterns = [
    path('users/', CreateUserView.as_view(), name='user-create'),

    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/<int:pk>/', TestDetailView.as_view(), name='test-detail'),

    path('tests/passed/', PassedTestListView.as_view(), name='passed-test-list'),
    path('tests/passed/<int:pk>/', PassedTestDetailView.as_view(), name='passed-test-detail'),
]
