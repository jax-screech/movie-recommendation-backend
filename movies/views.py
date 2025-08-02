from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Comment, Like, WatchProgress
from .serializers import MovieSerializer, CommentSerializer, WatchProgressSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        movie = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, movie=movie)
        if not created:
            like.delete()
            return Response({'message': 'Unliked'}, status=status.HTTP_200_OK)
        return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, pk=None):
        movie = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchProgressListCreateView(generics.ListCreateAPIView):
    serializer_class = WatchProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        movie_id = serializer.validated_data.get('movie_id')
        progress = serializer.validated_data.get('progress')

        existing = WatchProgress.objects.filter(user=self.request.user, movie_id=movie_id).first()
        if existing:
            existing.progress = progress
            existing.save()
        else:
            serializer.save(user=self.request.user)
