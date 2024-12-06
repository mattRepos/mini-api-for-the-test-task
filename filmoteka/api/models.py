from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

def validate_video_file(value):
    valid_mime_types = ['video/mp4', 'video/mpeg', 'video/avi', 'video/mkv']
    valid_extensions = ['.mp4', '.mpeg', '.avi', '.mkv']

    from mimetypes import guess_type
    mime_type, _ = guess_type(value.name)

    if mime_type not in valid_mime_types:
        raise ValidationError(f"Unsupported file type. Allowed types: {', '.join(valid_extensions)}")
    
    if not any(value.name.endswith(ext) for ext in valid_extensions):
        raise ValidationError(f"File extension must be one of: {', '.join(valid_extensions)}")

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    favorited_by = models.ManyToManyField(to=User, related_name="favorites", blank=True)
    file = models.FileField(verbose_name="Фильм", upload_to="movies/", validators=[validate_video_file])

    def __str__(self):
        return self.title
