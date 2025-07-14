from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, LikeViewSet, WatchlistViewSet

router = DefaultRouter()#obbject to hold all the  registered end points

router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')

urlpatterns = [
    path('', include(router.urls)),#then include all th endppoints regisstered under the router
]
