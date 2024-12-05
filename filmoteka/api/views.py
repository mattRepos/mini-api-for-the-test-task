from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Movie, Favorite
from .serializers import UserSerializer, MovieSerializer, FavoriteSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class FavoriteViewSet(viewsets.ViewSet):
    queryset = Favorite.objects.all()

    def list(self, request):
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add')
    def add_to_favorites(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='remove')
    def remove_from_favorites(self, request):
        user_id = request.data.get("user")
        movie_id = request.data.get("movie")
        try:
            favorite = Favorite.objects.get(user_id=user_id, movie_id=movie_id)
            favorite.delete()
            return Response({"message": "Removed from favorites"}, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            return Response({"error": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='user-favorites')
    def user_favorites(self, request, pk=None):
        favorites = Favorite.objects.filter(user_id=pk).select_related('movie')
        data = [{'id': fav.movie.id, 'title': fav.movie.title} for fav in favorites]
        return Response(data)
