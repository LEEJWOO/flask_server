from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
from concurrent.futures import ProcessPoolExecutor

def setup_driver():
    # Chrome 드라이버 설정을 정의합니다.
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # User-Agent 값을 변경합니다.
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver

def crawl_episode_comments(episode_number):
    driver = setup_driver()
    episode_url = f'https://comic.naver.com/webtoon/detail?titleId=764480&no={episode_number}&week=mon'
    driver.get(episode_url)
    wait = WebDriverWait(driver, 10)

    try:
        view_all_comments_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_view_comment')))
        view_all_comments_button.click()
    except TimeoutException:
        print(f"{episode_url} 전체 댓글 보기 버튼을 찾을 수 없었습니다!")
        driver.quit()
        return []

    comments = []
    start_time = time.time()

    while True:
        try:
            more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'u_cbox_btn_more')))
            driver.execute_script("arguments[0].click();", more_button)
        except TimeoutException:
            print("더 이상 로드할 댓글이 없습니다.")
            break

    page_comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_contents')
    comments.extend([comment.text for comment in page_comments])
    driver.quit()

    elapsed_time = time.time() - start_time
    log_time(episode_number, elapsed_time)

    comments_folder = os.path.join(os.getcwd(), 'Webtoon_Comments')
    os.makedirs(comments_folder, exist_ok=True)
    comment_filename = os.path.join(comments_folder, f'{episode_number}_comments.txt')
    with open(comment_filename, 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + "\n")

    print(f"Episode {episode_number} 크롤링 완료. 소요 시간: {elapsed_time:.2f}초")
    return comments, elapsed_time

def log_time(episode_number, elapsed_time):
    log_folder = os.path.join(os.getcwd(), 'Webtoon_Comments')
    os.makedirs(log_folder, exist_ok=True)  # 폴더가 없는 경우 생성
    log_filename = os.path.join(log_folder, 'crawling_time_log.txt')
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f'Episode {episode_number}: {elapsed_time:.2f} seconds\n')

def comments_crawler(start_episode, end_episode):
    total_time = 0
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = executor.map(crawl_episode_comments, range(start_episode, end_episode + 1))
    for _, time_taken in results:
        total_time += time_taken
    print(f"Total time taken for crawling from episode {start_episode} to {end_episode}: {total_time:.2f} seconds")
    return 0
