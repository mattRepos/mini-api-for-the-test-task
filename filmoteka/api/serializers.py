from rest_framework import serializers
from .models import User, Movie


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserWithFavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "favorites"]


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "rating", "file"]


class MovieWithFavoriteSerializer(serializers.ModelSerializer):

    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "rating", "is_favorite", "file"]

    def get_is_favorite(self, obj: Movie):
        return obj.id in self.context["user_favorites"]


class FavoriteAddRequestSerializer(serializers.Serializer):

    movie_id = serializers.IntegerField()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user
