from django.contrib import admin
from .models import Movie, Like, Watchlist

# Register your models here.
admin.site.register(Movie)
admin.site.register(Like)
admin.site.register(Watchlist)
