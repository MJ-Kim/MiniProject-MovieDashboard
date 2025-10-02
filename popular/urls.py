from django.urls import path

from popular.views import crawling_movies, dashboard

urlpatterns = [
    path("movies/", crawling_movies, name="crawling_movies"),
    path("dashboard/", dashboard),
]