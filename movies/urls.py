# movies/urls.py
from django.urls import path
from .views import TMDBFetchMoviesView

urlpatterns = [
    path('fetch/', TMDBFetchMoviesView.as_view(), name='fetch-movies'),
]
