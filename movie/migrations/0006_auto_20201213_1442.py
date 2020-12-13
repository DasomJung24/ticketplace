# Generated by Django 3.1.4 on 2020-12-13 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_auto_20201213_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actor',
            field=models.ManyToManyField(through='movie.MovieActor', to='movie.Actor'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(through='movie.MovieGenre', to='movie.Genre'),
        ),
        migrations.AlterField(
            model_name='movieactor',
            name='actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor_list', to='movie.actor'),
        ),
        migrations.AlterField(
            model_name='moviegenre',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genre_list', to='movie.genre'),
        ),
    ]
