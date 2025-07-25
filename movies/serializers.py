from rest_framework import serializers
from .models import Movie, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class MovieSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'