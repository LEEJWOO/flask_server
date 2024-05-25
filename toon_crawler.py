from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from concurrent.futures import ProcessPoolExecutor
import time
import os
import db


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver


def crawl_episode_comments(titleId, episode_number):
    driver = setup_driver()
    episode_url = f'https://comic.naver.com/webtoon/detail?titleId={titleId}&no={episode_number}'
    driver.get(episode_url)
    wait = WebDriverWait(driver, 1)
    comments = []

    start_time = time.time()  # 댓글 크롤링 시작 시간

    try:
        view_all_comments_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_view_comment')))
        view_all_comments_button.click()
    except TimeoutException:
        driver.quit()
        return comments

    while True:
        try:
            more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_more')))
            driver.execute_script("arguments[0].click();", more_button)
        except TimeoutException:
            break

    page_comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_contents')
    comments.extend([comment.text for comment in page_comments])
    driver.quit()

    end_time = time.time()  # 댓글 크롤링 종료 시간

    comments_folder = os.path.join(os.getcwd(), f'Webtoon_{titleId}')
    os.makedirs(comments_folder, exist_ok=True)
    comment_filename = os.path.join(comments_folder, f'comments_{titleId}_{episode_number}.txt')
    with open(comment_filename, 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + "\n")

    # 시간 로그를 파일에 저장
    with open(f"comments_crawler_time_log_{titleId}.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"Episode {episode_number} - Crawling Time: {end_time - start_time:.3f}s\n")

    return comments


def comments_crawler(titleId, end_episode, start_episode=1):
    start_time = time.time()  # 자연어 처리 시작 시간
    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(crawl_episode_comments, titleId, episode_number)
                   for episode_number in range(start_episode, end_episode + 1)]

        for future in futures:
            future.result()
    end_time = time.time()  # 자연어 처리 종료 시간
    total_time = end_time - start_time

    # 총 시간 기록을 파일에 저장
    with open(f"comments_crawler_time_log_{titleId}.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"Total Time for comments crawling: {total_time:.3f}s\n")

    return True


def star_crawler(titleId):
    driver = setup_driver()
    ratings = []
    page = 1
    last_episode = 0
    time_logs = []  # 시간 기록을 저장할 리스트
    try:
        while True:
            base_url = f'https://comic.naver.com/webtoon/list?titleId={titleId}&page={page}&sort=DESC'
            start_time = time.time()  # 페이지 로드 시작 시간
            driver.get(base_url)
            time.sleep(0.1)

            for i in range(1, 21):
                try:
                    start_episode_time = time.time()  # 에피소드 크롤링 시작 시간
                    episode_xpath = f'/html/body/div[1]/div/div[2]/div/div[1]/div[3]/ul/li[{i}]/a'
                    episode_link = driver.find_element(By.XPATH, episode_xpath)
                    episode_number = episode_link.get_attribute('href').split('no=')[1].split('&')[0]
                    star_rating = driver.find_element(By.XPATH,
                                                      f'/html/body/div[1]/div/div[2]/div/div[1]/div[3]/ul/li[{i}]/a/div[2]/div/span[1]/span').text
                    ratings.append({'episode': int(episode_number), 'star': float(star_rating)})
                    last_episode = max(last_episode, int(episode_number))
                    end_episode_time = time.time()  # 에피소드 크롤링 종료 시간
                    time_logs.append(f"Episode {episode_number} - Crawling Time: {end_episode_time - start_episode_time:.3f}s\n")
                except NoSuchElementException:
                    break
                except Exception as e:
                    print(f"Error fetching rating for episode {i} on page {page}: {str(e)}")
                    continue
            if len(ratings) < 20 * page:  # 별점 목록이 페이지당 20개 미만이면 마지막 페이지로 간주
                break
            end_page_time = time.time()  # 페이지 로드 종료 시간
            time_logs.append(f"Page {page} - Load Time: {end_page_time - start_time:.3f}s\n")
            page += 1
    finally:
        driver.quit()

    # 시간 로그를 파일에 저장
    with open("star_crawler_time_log.txt", "w", encoding="utf-8") as log_file:
        log_file.writelines(time_logs)

    stars_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'Webtoon_{titleId}')
    os.makedirs(stars_folder, exist_ok=True)
    star_filename = os.path.join(stars_folder, f'star_{titleId}.txt')
    with open(star_filename, 'w', encoding='utf-8') as file:
        for rating in ratings:
            file.write(f"Episode {rating['episode']}: {rating['star']}\n")

    record_id = db.create_stars(ratings)
    return record_id, last_episode
