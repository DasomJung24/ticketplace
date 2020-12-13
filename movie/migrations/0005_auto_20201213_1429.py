# Generated by Django 3.1.4 on 2020-12-13 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_auto_20201211_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actor',
            field=models.ManyToManyField(related_name='actor_list', through='movie.MovieActor', to='movie.Actor'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(related_name='genre_list', through='movie.MovieGenre', to='movie.Genre'),
        ),
    ]
