from django.urls import path
from .views import  RegisterView, CustomTokenObtainPairView, ProfileView, ChangePasswordView, DeleteUserView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('delete-account/', DeleteUserView.as_view(), name='delete-account'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
