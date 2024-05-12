import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import os

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
            driver.execute_script("arguments[0].click();", more_button) #more button(더 보기) 클릭시 항상 이렇게 호출하기!
        except TimeoutException:
            break

    page_comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_contents')
    comments.extend([comment.text for comment in page_comments])
    driver.quit()

    results_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Webtoon_Comments') #폴더에 저장하는 코드
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

            # 페이지에 별점 요소가 나타날 때까지 대기
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="rating_type"]')))

            # 페이지에 나열된 모든 에피소드에 대해 별점 수집
            for i in range(1, 21):  # 20개 에피소드가 최대
                try:
                    link_xpath = f'/html/body/div[1]/div/div[2]/div/div[1]/div[3]/ul/li[{i}]/a'
                    episode_link = driver.find_element(By.XPATH, link_xpath)
                    episode_number = episode_link.get_attribute('href').split('no=')[1].split('&')[0]
                    star_rating = episode_link.find_element(By.XPATH, '../div[2]/div/span[1]/span').text.strip()
                    if star_rating:
                        ratings.append(float(star_rating))
                        last_episode = max(last_episode, int(episode_number))
                except NoSuchElementException:
                    break  # 에피소드가 20개 미만인 경우 중단
                except Exception as e:
                    print(f"Error fetching rating for episode index {i} on page {page}: {str(e)}")
                    continue

            # 별점 목록이 20개 미만이면 마지막 페이지로 간주
            if len(ratings) % 20 > 0:
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