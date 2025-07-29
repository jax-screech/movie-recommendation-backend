from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # User + social login
    path('api/auth/', include('users.urls')),  # Custom endpoints (e.g., profile, Google login)
    path('api/auth/', include('dj_rest_auth.urls')),  # Login, logout, password reset
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Email/username registration
    path('api/', include('movies.urls')),  # Movie-related endpoints

    # OPTIONAL: keep this for redirect-based OAuth login (not used in frontend apps)
    path('accounts/', include('allauth.socialaccount.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
