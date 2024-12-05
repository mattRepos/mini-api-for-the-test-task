from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True,null=True)
    rating = models. FloatField(default=0.0)
    
    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='favorited_by', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} --> {self.movie.title}"
    
