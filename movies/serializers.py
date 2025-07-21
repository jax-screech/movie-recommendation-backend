# movies/serializers.py
from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


# movies/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer
from django.conf import settings

class TMDBFetchMoviesView(APIView):
    def get(self, request):
        api_key = settings.TMDB_API_KEY
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1"

        response = requests.get(url)
        if response.status_code != 200:
            return Response({"error": "Failed to fetch movies from TMDB."}, status=status.HTTP_502_BAD_GATEWAY)

        data = response.json().get('results', [])
        movies = []

        for item in data:
            movie, created = Movie.objects.get_or_create(
                tmdb_id=item['id'],
                defaults={
                    'title': item.get('title'),
                    'overview': item.get('overview'),
                    'release_date': item.get('release_date'),
                    'poster_path': item.get('poster_path'),
                }
            )
            movies.append(movie)

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
