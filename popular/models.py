from django.db import models

# Create your models here.
class MoviePopular(models.Model):
    platform = models.CharField("플랫폼", max_length=20)
    title = models.CharField("영화 제목", max_length=200)
    genre = models.CharField("영화 장르", max_length=100)
    release_date = models.DateField("개봉 날짜")
    rating = models.FloatField("평점")
    male_rating = models.FloatField("남성 평점")
    female_rating = models.FloatField("여성 평점")
    likes = models.IntegerField("좋아요 수")