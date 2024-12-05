from rest_framework import serializers
from .models import User,Movie,Favorite

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'created_at', 'updated_at']

class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'rating']

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movei = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'movie']
