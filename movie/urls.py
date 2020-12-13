from django.urls import path
from . import views

app_name = 'movie'
urlpatterns = [
    path('movies', views.MovieView.as_view()),
    path('movies/<int:movie_id>', views.MovieDetailView.as_view()),
]
