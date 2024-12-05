from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, MovieViewSet, FavoriteViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('movies', MovieViewSet, basename='movie')


favorite_list = FavoriteViewSet.as_view({
    'get': 'list',
    'post': 'add_to_favorites',
})

favorite_remove = FavoriteViewSet.as_view({
    'post': 'remove_from_favorites',
})

user_favorites = FavoriteViewSet.as_view({
    'get': 'user_favorites',
})

urlpatterns = [
    path('', include(router.urls)),
    path('favorites/', favorite_list, name='favorite-list'),
    path('favorites/remove/', favorite_remove, name='favorite-remove'),
    path('favorites/user/<int:pk>/', user_favorites, name='user-favorites'),
]
