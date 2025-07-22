from django.urls import path
from .views import register_user, CustomTokenObtainPairView,forgot_password
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/forgot-password/', forgot_password, name='forgot-password'),
]
