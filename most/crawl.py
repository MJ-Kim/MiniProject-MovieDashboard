from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def crawl_one_genre():
    driver = webdriver.Chrome()
    base_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%98%81%ED%99%94+%EC%B6%94%EC%B2%9C&ackey=mr0r2yhn"
    driver.get(base_url)
    movie_xpath = '//*[@id="main_pack"]/section[1]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/ul/li/div/a'

    links = driver.find_elements(By.XPATH, movie_xpath)

    hrefs = [link.get_attribute("href") for link in links]

    return hrefs


def click_other_genre():
    driver = webdriver.Chrome()
    base_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%98%81%ED%99%94+%EC%B6%94%EC%B2%9C&ackey=mr0r2yhn"
    driver.get(base_url)
    buttons = driver.find_elements(
        By.XPATH,
        '/html/body/div[3]/div[2]/div[1]/div[1]/section[1]/div/div[2]/div[2]/div/div[2]/div[1]/div/ul/li/a'
    )
    href_list = []
    # 순서대로 클릭
    for btn in buttons:
        btn.click()
        movie_xpath = '//*[@id="main_pack"]/section[1]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/ul/li/div/a'

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, movie_xpath))
        )
        links = driver.find_elements(By.XPATH, movie_xpath)

        href_list += [link.get_attribute("href") for link in links]
        time.sleep(1)

    return href_list


def crawl_one_page(driver, base_url):
    # base_url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&pkid=68&os=34307819&qvt=0&query=%EC%98%81%ED%99%94%20%EB%A3%A9%EB%B0%B1'
    # driver = webdriver.Chrome()
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)

    dd_xpath = '/html/body/div[3]/div[2]/div[1]/div[1]/div[3]/div[2]/div[2]/div/div[1]/dl/div/dd'

    # dds = driver.find_elements(By.XPATH, dd_xpath)
    dds = driver.find_elements(By.XPATH, "//div[@id='main_pack']//dl/div/dd")

    try:
        title = driver.find_element(
            By.CSS_SELECTOR, "div.title_area.type_keep._title_area h2 span strong"
        ).text.strip()
    except:
        title = None
        print(f'{base_url} has no title')

    # values = [dd.text for dd in dds]
    # print(values)
    if len(dds) >= 3:
        genre_parts = driver.execute_script(
            "return Array.from(arguments[0].childNodes).map(n=>n.textContent.trim()).filter(x=>x);",
            dds[0]
        )
        genre = genre_parts[0] if genre_parts else None

        # dd[1] = 개봉일
        release_date = dds[1].text.strip() if len(dds) > 1 else None

        # dd[2] = 평점
        rating = dds[2].text.strip() if len(dds) > 2 else None

    else:
        genre, release_date, rating = None, None, None
        print(f'{base_url} has no genre, release_date, rating')

    # --- likes 가져오기 ---
    # likes_element = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "span._like_count._count"))
    # )
    # likes = likes_element.text.strip()
    likes = driver.execute_script(
        "return document.querySelector('span._like_count._count')?.innerText || null;"
    )
    # --- 성별 평점 ---
    try:
        male_selector = "div.area_card_male span.area_star_number span"


        male_rating = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, male_selector))
        ).text.strip()

        male_rating = float(male_rating)
    except:
        male_rating = None
        print(f"{base_url} has no male rating")


    try:
        female_selector = "div.area_card_female span.area_star_number span"
        female_rating = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, female_selector))
        ).text.strip()
        female_rating = float(female_rating)
    except:
        female_rating = None
        print(f"{base_url} has no female rating")



    return {
        "title": title,
        "genre": genre,
        "release_date": release_date,
        "rating": rating,
        "likes": likes,
        "male_rating": male_rating,
        "female_rating": female_rating
    }







if __name__ == "__main__":
    # href_list = click_other_genre()
    #
    # for href in href_list:
    #     print(href)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # UI 안 보이게
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    # webdriver 탐지 회피
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    base_url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&pkid=68&os=35438055&qvt=0&query=%EB%82%98%20%ED%98%BC%EC%9E%90%EB%A7%8C%20%EB%A0%88%EB%B2%A8%EC%97%85%20%EB%A6%AC%EC%96%B4%EC%9B%A8%EC%9D%B4%ED%81%AC%EB%8B%9D'
    movie_info = crawl_one_page(driver, base_url)
    print(movie_info)