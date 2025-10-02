from django.db import models

# Create your models here.
class MoviePopular(models.Model):
    platform = models.CharField("플랫폼", max_length=20)  # 넷플릭스, 왓챠, 네이버 등
    title = models.CharField("영화 제목", max_length=200) # 영화 제목
    genre = models.CharField("영화 장르", max_length=100) # 장르 (단일 값)
    release_date = models.DateField("개봉 날짜")    # 개봉일
    rating = models.FloatField("평점")             # 전체 평점
    male_rating = models.FloatField("남성 평점")    # 남성 평점
    female_rating = models.FloatField("여성 평점")  # 여성 평점
