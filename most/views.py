from django.shortcuts import render
from selenium import webdriver
from collections import defaultdict
from most.crawl import crawl_one_page, click_other_genre
import time
import random
from collections import Counter
import json

# Create your views here.
def most_view(request):
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # UI 안 보이게
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)
    #
    # driver = webdriver.Chrome(options=options)
    #
    # # webdriver 탐지 회피
    # driver.execute_cdp_cmd(
    #     "Page.addScriptToEvaluateOnNewDocument",
    #     {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    # )
    #
    # href_list = click_other_genre()
    # results = []
    # for href in href_list:
    #     movie_info = crawl_one_page(driver=driver, base_url=href)
    #     results.append(movie_info)
    #     time.sleep(random.uniform(1.5, 3.0))
    #
    # with open("results.json", "w", encoding="utf-8") as f:
    #     json.dump(results, f, ensure_ascii=False, indent=4)

    with open("results.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    results = list({m["title"]: m for m in results}.values())

    # 장르 필터링
    genres = [m["genre"] for m in results if m.get("genre") not in (None, "", "None")]
    genre_counts = Counter(genres)

    # 평점 Top 15
    top_movies = sorted(
        [m for m in results if m.get("rating")],
        key=lambda x: x["rating"],
        reverse=True
    )[:15]

    # --- 성별 평점 분포 ---
    male_titles = [m["title"] for m in results if m.get("male_rating") and m.get("female_rating")]
    male_ratings = [m["male_rating"] for m in results if m.get("male_rating")]
    female_ratings = [m["female_rating"] for m in results if m.get("female_rating")]

    # --- 남녀 평점 차이 Top 5 ---
    diff_movies = []
    for m in results:
        if m.get("male_rating") and m.get("female_rating"):
            diff = abs(float(m["male_rating"]) - float(m["female_rating"]))
            diff_movies.append((m["title"], diff))
    diff_top5 = sorted(diff_movies, key=lambda x: x[1], reverse=True)[:5]

    # --- 장르별 남/여 평점 ---
    genre_ratings = defaultdict(lambda: {"male": [], "female": []})

    for m in results:
        genre = m.get("genre")
        if genre and genre not in (None, "", "None"):
            if m.get("male_rating"):
                genre_ratings[genre]["male"].append(float(m["male_rating"]))
            if m.get("female_rating"):
                genre_ratings[genre]["female"].append(float(m["female_rating"]))

    genre_labels = []
    male_avg = []
    female_avg = []

    for genre, vals in genre_ratings.items():
        if vals["male"] or vals["female"]:
            genre_labels.append(genre)
            male_avg.append(round(sum(vals["male"]) / len(vals["male"]), 2) if vals["male"] else 0)
            female_avg.append(round(sum(vals["female"]) / len(vals["female"]), 2) if vals["female"] else 0)

    context = {
        "genres": list(genre_counts.keys()),
        "genre_counts": list(genre_counts.values()),
        "movie_titles": [m["title"] for m in top_movies],
        "movie_ratings": [m["rating"] for m in top_movies],
        # 성별 평점 분포
        "male_titles": male_titles,
        "male_ratings": male_ratings,
        "female_ratings": female_ratings,

        # 성별 평점 차이
        "diff_titles": [d[0] for d in diff_top5],
        "diff_values": [d[1] for d in diff_top5],

        "genre_labels": genre_labels,
        "male_avg": male_avg,
        "female_avg": female_avg,
    }

    return render(request, "most/dashboard.html", context)


# def dashboard(request):
#     # 예시 데이터 (크롤링한 걸 DB에서 불러온다고 가정)
#     genres = ["드라마", "액션", "로맨스", "코미디", "스릴러"]
#     genre_counts = [12, 8, 6, 4, 3]
#
#     # 평점 Top 15
#     top_movies = [
#         {"title": "영화A", "rating": 9.5},
#         {"title": "영화B", "rating": 9.3},
#         {"title": "영화C", "rating": 9.0},
#         {"title": "영화D", "rating": 8.9},
#         {"title": "영화E", "rating": 8.8},
#         {"title": "영화F", "rating": 8.7},
#         {"title": "영화G", "rating": 8.6},
#         {"title": "영화H", "rating": 8.5},
#         {"title": "영화I", "rating": 8.4},
#         {"title": "영화J", "rating": 8.3},
#         {"title": "영화K", "rating": 8.2},
#         {"title": "영화L", "rating": 8.1},
#         {"title": "영화M", "rating": 8.0},
#         {"title": "영화N", "rating": 7.9},
#         {"title": "영화O", "rating": 7.8},
#     ]
#
#     return render(request, "most/dashboard.html", {
#         "genres": genres,
#         "genre_counts": genre_counts,
#         "movie_titles": [m["title"] for m in top_movies],
#         "movie_ratings": [m["rating"] for m in top_movies],
#     })