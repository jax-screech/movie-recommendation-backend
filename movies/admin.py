from django.contrib import admin
from .models import Movie, Like, Watchlist

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date', 'rating')
    search_fields = ('title', 'genre')
    list_filter = ('genre', 'release_date')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'liked_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('liked_at',)


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'added_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('added_at',)
