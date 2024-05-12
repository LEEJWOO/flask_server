import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
#from selenium.common.exceptions import WebDriverException

import os
#import time

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

    results_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Webtoon_Comments')  # 저장 코드
    os.makedirs(results_folder, exist_ok=True)
    comment_filename = os.path.join(results_folder, f'{episode_number}_comments.txt')
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
    last_episode = 0  # 마지막 회차 번호를 추적하기 위한 변수

    try:
        while True:
            base_url = f'https://comic.naver.com/webtoon/list?titleId={titleId}&page={page}&sort=DESC'
            driver.get(base_url)
            time.sleep(0.1)  # 페이지 로드를 보장하기 위해 잠시 대기 (동적 대기로 변경 예정)

            current_page_ratings = []
            episodes = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[1]/div[3]/ul/li/div/a')
            for episode in episodes:
                episode_number = int(episode.get_attribute('href').split('no=')[1].split('&')[0])
                try:
                    xpath = f'/html/body/div[1]/div/div[2]/div/div[1]/div[3]/ul/li[{episode_number}]/a/div[2]/div/span[1]/span'
                    star_rating = driver.find_element(By.XPATH, xpath).text
                    if star_rating:
                        current_page_ratings.append(float(star_rating))
                        last_episode = max(last_episode, episode_number)
                except Exception as e:
                    print(f"Error fetching rating for episode {episode_number}: {str(e)}")
                    continue

            if len(current_page_ratings) < 20:  # 20개 미만이면 마지막 페이지로 간주, 루프 종료
                ratings.extend(current_page_ratings)
                break

            ratings.extend(current_page_ratings)
            page += 1  # 다음 페이지로 넘어가기

    finally:
        driver.quit()

    ratings.reverse()# 데이터를 역순으로 정렬하여 1화부터 마지막 화까지 순서대로 배열

    # 결과를 파일에 저장
    results_folder = os.path.join(os.getcwd(), 'Webtoon_Ratings')
    os.makedirs(results_folder, exist_ok=True)
    ratings_file_path = os.path.join(results_folder, f'{titleId}_ratings.txt')
    with open(ratings_file_path, 'w', encoding='utf-8') as file:
        for episode, rating in enumerate(ratings, 1):
            file.write(f'{episode}, {rating}\n')
            print(f'{episode}, {rating}')  # 콘솔에 출력

    return ratings, last_episode


if __name__ == "__main__":
    title_id = 764480  # 예시 웹툰 ID
    ratings, last_episode = star_crawler(title_id)
    print(f"Last crawled episode: {last_episode}")
    print("Ratings:", ratings)