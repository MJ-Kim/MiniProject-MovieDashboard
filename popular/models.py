from django.db import models

# Create your models here.
class MoviePopular(models.Model):
    platform = models.CharField("플랫폼", max_length=20)
    title = models.CharField("영화 제목", max_length=200)
    genre = models.CharField("영화 장르", max_length=100)
    release_date = models.DateField("개봉 날짜", blank=True, null=True)
    rating = models.FloatField("평점", blank=True)
    male_rating = models.FloatField("남성 평점", blank=True)
    female_rating = models.FloatField("여성 평점", blank=True)
    likes = models.IntegerField("좋아요 수", blank=True, default=0)
    created_at = models.DateTimeField("크롤링 날짜", auto_now_add=True)