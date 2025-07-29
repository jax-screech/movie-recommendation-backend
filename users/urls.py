# urls.py
from django.urls import path
from .views import profile_view, RegisterView, LoginView, ForgotPasswordView, ResetPasswordView, GoogleLogin

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/', profile_view, name='profile'),
    path('google-login/', GoogleLogin.as_view(), name='google-login'),
]
