from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Movie
from .serializers import (
    UserSerializer,
    MovieSerializer,
    FavoriteAddRequestSerializer,
    UserDetailSerializer,
    RegistrationSerializer,
    UserWithFavoritesSerializer,
    MovieWithFavoriteSerializer,
)
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().only("id", "username")
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return (
                User.objects.all()
                .only("id", "username", "favorites")
                .prefetch_related("favorites")
            )
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserWithFavoritesSerializer
        return super().get_serializer_class()


    @action(
        detail=False,
        methods=["GET"],
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def get_me(self, request: Request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.prefetch_related("favorited_by")
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        if (user := self.request.user) and self.action != "favorites_handle":
            favorite_ids = user.favorites.values_list("id", flat=True)
            kwargs["context"] = kwargs.get("context", {})
            kwargs["context"]["user_favorites"] = list(favorite_ids)
            return MovieWithFavoriteSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    @action(
        detail=False,
        methods=["GET", "POST", "DELETE"],
        url_path="favorites",
        permission_classes=[IsAuthenticated],
    )
    def favorites_handle(self, request: Request):
        handlers = {
            "get": self.get_favorites,
            "post": self.set_favorite,
            "delete": self.delete_favorite,
        }
        return handlers[request.method.lower()](request)

    def get_favorites(self, request: Request):
        user = request.user
        favorites = user.favorites.all()
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)

    def get_movie_from_request_data(self, data: dict) -> Movie:
        serializer = FavoriteAddRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        movie_id = serializer.validated_data.get("movie_id")
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise NotFound(detail="Movie does not exist")
        return movie

    def set_favorite(self, request: Request):
        movie = self.get_movie_from_request_data(request.data)
        user = request.user
        user.favorites.add(movie)
        return Response(self.get_serializer(movie).data)

    def delete_favorite(self, request: Request):
        movie = self.get_movie_from_request_data(request.data)
        user = request.user
        favorite = user.favorites.filter(movie=movie)
        favorite.delete()
        return Response(status=204)


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED,
        )
