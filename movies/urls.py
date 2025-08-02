from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MovieViewSet, WatchProgressListCreateView

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls)),
    path('progress/', WatchProgressListCreateView.as_view(), name='watch-progress'),
]
