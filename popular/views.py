from django.db.models.aggregates import Max
from django.shortcuts import render, redirect
from .models import MoviePopular
from .crawler import run_crawling
from datetime import datetime
import re
from collections import Counter

# Create your views here.
def crawling_movies(request):
    results = run_crawling()  # 크롤링 실행 → 결과 리스트 반환

    for data in results:
        release_date = None
        if data.get("release_date"):
            date_text = data["release_date"].strip()
            # 정규식으로 YYYY.MM.DD. 패턴만 필터링
            if re.match(r"^\d{4}\.\d{2}\.\d{2}\.$", date_text):
                try:
                    release_date = datetime.strptime(date_text, "%Y.%m.%d.").date()
                except:
                    release_date = None

        # DB 저장 (플랫폼 + 제목 동일하면 업데이트)
        MoviePopular.objects.update_or_create(
            platform=data.get("platform", ""),  # 플랫폼
            title=data.get("title", ""),        # 영화 제목
            defaults={
                "genre": data.get("genre", ""),
                "release_date": release_date,
                "rating": float(data["rating"]) if data.get("rating") else 0.0,
                "male_rating": float(data["male_rating"]) if data.get("male_rating") else 0.0,
                "female_rating": float(data["female_rating"]) if data.get("female_rating") else 0.0,
                "likes": int(data["count_likes"]) if data.get("count_likes") else 0,
            },
        )

    return redirect(f"/")

def dashboard(request):
    # 좋아요 순 Top 10
    top_likes = (
        MoviePopular.objects
        .values("title")
        .annotate(max_likes=Max("likes"))
        .order_by("-max_likes")[:10]
    )

    # 평점 순 Top 10
    top_rating = (
        MoviePopular.objects
        .values("title")
        .annotate(max_rating=Max("rating"))
        .order_by("-max_rating")[:10]
    )

    # 남성 평점 순 Top 10
    top_male = (
        MoviePopular.objects
        .values("title")
        .annotate(max_rating=Max("male_rating"))
        .order_by("-max_rating")[:10]
    )

    # 여성 평점 순 Top 10
    top_female = (
        MoviePopular.objects
        .values("title")
        .annotate(max_rating=Max("female_rating"))
        .order_by("-max_rating")[:10]
    )

    # 플랫폼별 장르 카운트
    movies = MoviePopular.objects.all()
    platform_genre_data = {}
    for platform in movies.values_list("platform", flat=True).distinct():
        genres = movies.filter(platform=platform).values_list("genre", flat=True)
        genre_count = dict(Counter(genres))
        platform_genre_data[platform] = genre_count

    context = {
        "top_likes": top_likes,
        "top_rating": top_rating,
        "top_male": top_male,
        "top_female": top_female,
        "platform_genre_data": platform_genre_data,
    }
    return render(request, "popular/dashboard.html", context)