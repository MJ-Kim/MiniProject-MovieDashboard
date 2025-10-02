from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import datetime
from urllib.parse import urljoin

# 1. 플랫폼명과 영화 url 수집 함수
def fetch_platform_links(driver):
    base_url = "https://search.naver.com/search.naver"

    url = "https://search.naver.com/search.naver?query=영화+추천"
    driver.get(url)

    platform_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.cm_content_area._popular_section")
        )
    )

    platform_tabs = platform_section.find_elements(By.CSS_SELECTOR, "div.filter_tab_area ul > li")

    platform_links = {}
    for tab in platform_tabs:
        platform_name = tab.text.strip()
        tab.click()
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        # 상대경로 링크를 절대경로로 변환
        links = [
            urljoin(base_url, a["href"])
            for a in soup.select(
                "div.cm_content_area._popular_section div.info_area ul > li > div > a"
            )
        ]
        platform_links[platform_name] = links

    return platform_links


# 2. 영화 상세 정보 수집 함수
def fetch_movie_detail(driver, platform, url):
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # 제목
    try:
        title = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#main_pack h2 span strong"))
        ).text.strip()
    except:
        title = None

    # 장르
    try:
        genre_dd = driver.find_element(
            By.CSS_SELECTOR, "#main_pack dl > div:nth-child(1) > dd"
        )
        genre_parts = driver.execute_script(
            "return Array.from(arguments[0].childNodes).map(n => n.textContent.trim()).filter(x => x);",
            genre_dd
        )
        genre = genre_parts[0] if genre_parts else None
    except:
        genre = None

    # 개봉일 (문자열 → datetime 변환)
    try:
        release_text = driver.find_element(
            By.CSS_SELECTOR, "#main_pack dl > div:nth-child(2) > dd"
        ).text.strip()
        release_date = datetime.strptime(release_text, "%Y.%m.%d").date()
    except:
        release_date = None

    # 평점
    try:
        rating_text = driver.find_element(
            By.CSS_SELECTOR, "#main_pack dl > div:nth-child(3) > dd"
        ).text.strip()
        rating = float(rating_text.split()[0]) if rating_text else None
    except:
        rating = None

    # 남성 평점
    try:
        male_rating_text = driver.find_element(
            By.CSS_SELECTOR, "#main_pack ul li a div:nth-child(2) div:nth-child(1) span:nth-child(2) span"
        ).text.strip()
        male_rating = float(male_rating_text)
    except:
        male_rating = None

    # 여성 평점
    try:
        female_rating_text = driver.find_element(
            By.CSS_SELECTOR, "#main_pack ul li a div:nth-child(2) div:nth-child(2) span:nth-child(2) span"
        ).text.strip()
        female_rating = float(female_rating_text)
    except:
        female_rating = None

    # 좋아요 수
    count_likes_elem = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "span._like_count._count")
        )
    )
    count_likes = count_likes_elem.text.strip()
    count_likes = int(count_likes.replace(",", "")) if count_likes else 0

    return {
        "platform": platform,
        "title": title,
        "genre": genre,
        "release_date": release_date,
        "rating": rating,
        "male_rating": male_rating,
        "female_rating": female_rating,
        "count_likes": count_likes,
    }


# 3. 실행 함수
def run_crawling():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("lang=ko_KR")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=chrome_options)

    platform_links = fetch_platform_links(driver)
    all_results = []

    for platform, links in platform_links.items():
        for link in links:
            try:
                info = fetch_movie_detail(driver, platform, link)
                all_results.append(info)
            except Exception as e:
                print(f"❌ Error fetching {platform} - {link}: {e}")

    driver.quit()
    return all_results

