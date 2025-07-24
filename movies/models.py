from django.db import models
from users.models import CustomUser

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=10)
    genre = models.CharField(max_length=100)
    poster_url = models.URLField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')
