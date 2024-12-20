# Generated by Django 5.1.4 on 2024-12-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_movie_favorited_by_delete_favorite"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="file",
            field=models.FileField(
                default=1, upload_to="movies/", verbose_name="Фильм"
            ),
            preserve_default=False,
        ),
    ]
