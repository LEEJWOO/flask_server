from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
    last_episode = 0

    try:
        while True:
            base_url = f'https://comic.naver.com/webtoon/list?titleId={titleId}&page={page}&sort=DESC'
            driver.get(base_url)
            wait = WebDriverWait(driver, 10)

            # 변경: 요소가 클릭 가능할 때까지 대기
            wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="rating_type"]')))
            current_page_ratings = []
            episodes = driver.find_elements(By.CSS_SELECTOR, 'td.title > a')

            for episode in episodes:
                episode_number = episode.get_attribute('href').split('no=')[1]
                try:
                    # 변경: 요소의 텍스트를 직접 접근
                    star_rating = episode.find_element(By.XPATH, './following-sibling::td[@class="rating_type"]/strong').text
                    current_page_ratings.append(float(star_rating))
                    last_episode = max(last_episode, int(episode_number))
                except Exception as e:
                    print(f"Error fetching rating for episode {episode_number}: {str(e)}")
                    continue

            if len(current_page_ratings) < 20:  # 20개 미만인 경우 마지막 페이지로 간주
                ratings.extend(current_page_ratings)
                break

            ratings.extend(current_page_ratings)
            page += 1  # 다음 페이지로 이동

    finally:
        driver.quit()

    if not ratings:  # 별점 데이터가 없는 경우 처리
        return None, 0

    return ratings, last_episode


if __name__ == "__main__":
    title_id = 764480  # 예시 웹툰 ID
    ratings, last_episode = star_crawler(title_id)
    print(f"Last crawled episode: {last_episode}")
    print("Ratings:", ratings)