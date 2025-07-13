from django.db import models
from users.models import CustomUser
# Create your models here.

# the movie catalog that the users will interact with
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()        
    poster_url = models.URLField(blank=True)
    rating = models.FloatField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# to track likes from the users to movies for more recommendations
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)# who
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)# which movie was liked
    liked_at = models.DateTimeField(auto_now_add=True)# when it was liked

    class Meta:
        unique_together = ('user', 'movie')# to ensere a user likes a movie only once

    def __str__(self):
        return f"{self.user.username} likes {self.movie.title}"

# to track which movies a user has saved to watch later
class Watchlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)# by who
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)# which movie
    added_at = models.DateTimeField(auto_now_add=True)# when

    class Meta:
        unique_together = ('user', 'movie')# to ensure a movie appears only once in a users watchlist

    def __str__(self):
        return f"{self.movie.title} in {self.user.username}'s watchlist"
