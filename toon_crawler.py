from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
import db
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# 로그 설정
logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # 0521 수정 : 로그 설정 추가

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver

def crawl_episode_comments(titleId, episode_number):
    start_time = time.time()  # 0521 수정 : 시작 시간 기록
    driver = setup_driver()
    episode_url = f'https://comic.naver.com/webtoon/detail?titleId={titleId}&no={episode_number}'
    driver.get(episode_url)
    wait = WebDriverWait(driver, 2)
    setup_time = time.time() - start_time  # 0521 수정 : 드라이버 설정 시간 기록

    try:
        view_all_comments_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_view_comment')))
        view_all_comments_button.click()
    except TimeoutException:
        logging.error(f"TimeoutException: View all comments button not found for {titleId} episode {episode_number}")  # 0521 수정 : 로그 기록 추가
        driver.quit()
        return []
    comments_button_time = time.time() - start_time  # 0521 수정 : 댓글 버튼 클릭 시간 기록

    comments = []
    while True:
        try:
            more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_more')))
            driver.execute_script("arguments[0].click();", more_button)  # more button(더 보기) 클릭시 항상 이렇게 호출하기!
        except TimeoutException:
            break

    comments_loading_time = time.time() - start_time  # 0521 수정 : 더 보기 버튼 클릭 시간 기록

    page_comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_contents')
    comments.extend([comment.text for comment in page_comments])
    driver.quit()
    comments_extraction_time = time.time() - start_time  # 0521 수정 : 댓글 추출 시간 기록

    comments_folder = os.path.join(os.getcwd(), f'Webtoon_{titleId}')  # 폴더에 저장하는 코드
    os.makedirs(comments_folder, exist_ok=True)
    comment_filename = os.path.join(comments_folder, f'comments_{titleId}_{episode_number}.txt')
    with open(comment_filename, 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + "\n")
    save_time = time.time() - start_time  # 0521 수정 : 파일 저장 시간 기록

    with open("time_log.txt", "a", encoding="utf-8") as log_file:  # 0521 수정 : 로그 파일에 기록 추가
        log_file.write(f"Episode {episode_number} - Setup: {setup_time:.3f}s, Button: {comments_button_time:.3f}s, Loading: {comments_loading_time:.3f}s, Extraction: {comments_extraction_time:.3f}s, Save: {save_time:.3f}s\n")

    return comments

def comments_crawler(titleId, end_episode):
    logging.info(f"Starting comments crawling for titleId {titleId}")  # 0521 수정 : 로그 추가
    comments = []

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_episode = {executor.submit(crawl_episode_comments, titleId, episode_number): episode_number for episode_number in range(1, end_episode + 1)}
        for future in as_completed(future_to_episode):
            episode_number = future_to_episode[future]
            try:
                episode_comments = future.result()
                if episode_comments:
                    comments.extend(episode_comments)
            except Exception as e:
                logging.error(f"Error crawling comments for episode {episode_number} of titleId {titleId}: {e}")

    logging.info(f"Comments crawling completed for titleId {titleId}")  # 0521 수정 : 로그 추가
    return comments

def star_crawler(titleId):
    logging.info(f"Starting star crawling for titleId {titleId}")  # 0521 수정 : 로그 추가
    driver = setup_driver()
    ratings = []
    page = 1
    last_episode = 0
    try:
        while True:
            base_url = f'https://comic.naver.com/webtoon/list?titleId={titleId}&page={page}&sort=DESC'
            driver.get(base_url)
            time.sleep(0.1)

            for i in range(1, 21):
                try:
                    episode_xpath = f'/html/body/div[1]/div/div[2]/div/div[1]/div[3]/ul/li[{i}]/a'
                    episode_link = driver.find_element(By.XPATH, episode_xpath)
                    episode_number = episode_link.get_attribute('href').split('no=')[1].split('&')[0]
                    star_rating = driver.find_element(By.XPATH,
                                                      f'/html/body/div[1]/div/div[2]/div/div[1]/div[3]/ul/li[{i}]/a/div[2]/div/span[1]/span').text
                    ratings.append({'episode': int(episode_number), 'star': float(star_rating)})
                    last_episode = max(last_episode, int(episode_number))
                except NoSuchElementException:  # 오류 메시지 자주 발생하나 치명적 오류는 아님
                    logging.error(f"NoSuchElementException: Element not found on page {page} for episode {i}")  # 0521 수정 : 로그 기록 추가
                    break
                except Exception as e:
                    logging.error(f"Error fetching rating for episode {i} on page {page}: {str(e)}")  # 0521 수정 : 로그 기록 추가
                    continue
            if len(ratings) < 20 * page:  # 별점 목록이 페이지당 20개 미만이면 마지막 페이지로 간주
                break
            page += 1
    finally:
        driver.quit()

    stars_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'Webtoon_{titleId}')
    os.makedirs(stars_folder, exist_ok=True)
    star_filename = os.path.join(stars_folder, f'star_{titleId}.txt')
    with open(star_filename, 'w', encoding='utf-8') as file:
        for rating in ratings:
            file.write(f"Episode {rating['episode']}: {rating['star']}\n")

    record_id = db.create_stars(ratings)
    logging.info(f"Star crawling completed for titleId {titleId}")  # 0521 수정 : 로그 추가
    return record_id, last_episode