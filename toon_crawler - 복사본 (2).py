from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

import os
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def crawl_episode_comments(titleId, episode_number):
    driver = setup_driver()
    episode_url = f'https://comic.naver.com/webtoon/detail?titleId={titleId}&no={episode_number}'
    driver.get(episode_url)
    wait = WebDriverWait(driver, 10)

    try:
        view_all_comments_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_view_comment')))
        view_all_comments_button.click()
    except TimeoutException:
        driver.quit()
        return []

    comments = []
    while True:
        try:
            more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_more')))
            driver.execute_script("arguments[0].click();", more_button)
        except TimeoutException:
            break

    page_comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_contents')
    comments.extend([comment.text for comment in page_comments])
    driver.quit()

    comments_folder = os.path.join(os.getcwd(), 'Webtoon_Comments') # 저장 코드
    os.makedirs(comments_folder, exist_ok=True)
    comment_filename = os.path.join(comments_folder, f'{episode_number}_comments.txt')
    with open(comment_filename, 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + "\n")

    return comments

def comments_crawler(titleId, start_episode, end_episode):
    comments = []
    for episode_number in range(start_episode, end_episode + 1):
        episode_comments = crawl_episode_comments(titleId, episode_number)
        comments.extend(episode_comments)
    return comments


def star_crawler(titleId):
    driver = setup_driver()
    ratings = []
    page = 1
    last_episode = 0

    try:
        while True:
            url = f"https://comic.naver.com/webtoon/list?titleId={titleId}&page={page}&sort=DESC"
            driver.get(url)
            time.sleep(0.5)  # 페이지 로드를 위한 대기

            # XPath를 사용하여 별점을 추출
            stars_elements = driver.find_elements(By.XPATH, "//div[@class='rating_type']/strong")
            episode_elements = driver.find_elements(By.XPATH, "//td[@class='title']/a")

            if not stars_elements:
                break  # 별점 정보가 없으면 종료합니다.

            for star, episode in zip(stars_elements, episode_elements):
                rating = float(star.text)
                ratings.append(rating)
                episode_no = episode.get_attribute('href').split('no=')[1].split('&')[0]
                last_episode = max(last_episode, int(episode_no))

            if len(stars_elements) < 20:  # 20개 미만이면 마지막 페이지로 간주
                break

            page += 1  # 다음 페이지로 이동
    finally:
        driver.quit()

    return ratings, last_episode

if __name__ == "__main__":
    title_id = 764480  # 예시 웹툰 ID
    ratings, last_episode = star_crawler(title_id)
    print(f"Last crawled episode: {last_episode}")
    print("Ratings:", ratings)