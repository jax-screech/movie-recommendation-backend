# movies/models.py
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    poster_path = models.URLField()
    release_date = models.DateField(null=True, blank=True)
    tmdb_id = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.title
