from django.urls import path

from .views import RegisterView, PasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('password/', PasswordView.as_view(), name='user-password'),
]
