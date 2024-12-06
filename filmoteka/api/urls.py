from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, MovieViewSet, RegistrationView

router = DefaultRouter(trailing_slash=False)
router.register("users", UserViewSet, basename="user")
router.register("movies", MovieViewSet, basename="movie")

urlpatterns = [
    path("", include(router.urls)),
    path("register", RegistrationView.as_view()),
]
