from django.db import models

# Create your models here.

class MostMovie(models.Model):
    title = models.CharField("영화 제목", max_length=100)
    genre = models.CharField("장르", max_length=100)
    rating = models.FloatField("평점")
    release_date = models.DateTimeField("출시 날짜")
    male_rating = models.FloatField("남성 평점")
    female_rating = models.FloatField("여성 평점")
