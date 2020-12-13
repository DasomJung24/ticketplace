from django.db import models


class Movie(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    running_time = models.IntegerField()
    release_date = models.DateField(auto_now_add=False, auto_now=False)
    director = models.CharField(max_length=50)
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE)
    image = models.URLField()
    summary = models.TextField()
    audience_score = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    netizen_score = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    reporter_critic_score = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    genre = models.ManyToManyField('Genre', through='MovieGenre')
    actor = models.ManyToManyField('Actor', through='MovieActor')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'movies'


class Country(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'countries'


class Rating(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ratings'


class MovieGenre(models.Model):
    objects = models.Manager()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_genre'


class Genre(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genre'


class MovieActor(models.Model):
    objects = models.Manager()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_actor'


class Actor(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'actors'
