from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Like, Watchlist
from .serializers import MovieSerializer, LikeSerializer, WatchlistSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['genre', 'rating']
    search_fields = ['title', 'description']
    ordering_fields = ['release_date', 'rating']
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
