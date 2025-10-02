from django.urls import path

from popular.views import crawling_movies

urlpatterns = [
    path("movies/", crawling_movies),
]