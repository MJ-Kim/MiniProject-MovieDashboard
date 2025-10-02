from django.shortcuts import render
from .models import MoviePopular
from .crawler import run_crawling
from datetime import datetime
import re

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

    # 저장된 영화 리스트 (좋아요 순 정렬)
    movies = MoviePopular.objects.all().order_by("-likes")

    context = {
        'movies':movies
    }

    return render(request, "popular/movies.html", context)