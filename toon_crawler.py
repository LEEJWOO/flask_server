from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
import db


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    # User-Agent 값을 변경, 크롤링 방지 우회.
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    return webdriver.Chrome(options=options)


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
            driver.execute_script("arguments[0].click();", more_button)  # more button(더 보기) 클릭시 항상 이렇게 호출하기!
        except TimeoutException:
            break

    page_comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_contents')
    comments.extend([comment.text for comment in page_comments])
    driver.quit()

    # TODO 크롤러 : Webtoon_titleID폴더 → 파일명 : comments_titleid_episodeno 변경!!
    comments_folder = os.path.join(os.getcwd(), f'Webtoon_{titleId}')  # 폴더에 저장하는 코드
    os.makedirs(comments_folder, exist_ok=True)
    comment_filename = os.path.join(comments_folder, f'comments_{titleId}_{episode_number}.txt')
    with open(comment_filename, 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + "\n")

    return comments
'''
comments_folder = os.path.join(os.getcwd(), 'Webtoon_824261')
    os.makedirs(comments_folder, exist_ok=True)
    comment_filename = os.path.join(comments_folder, f'comments_824261_{episode_number}.txt')

'''

# TODO 매개변수 변경 (url)
def comments_crawler(titleId, start_episode, end_episode):
    comments = []
    for episode_number in range(start_episode, end_episode + 1):
        episode_comments = crawl_episode_comments(titleId, episode_number)
        comments.extend(episode_comments)
    return comments

# TODO 매개변수 변경 (url)
def star_crawler(titleId): #크롤링 완료시 바로 star콜렉션에 JSON형태로 저장 후 starid 를 웹툰 콜렉션에 저장
    driver = setup_driver()
    ratings = []
    page = 1
    last_episode = 0
    try:
        while True:
            base_url = f'https://comic.naver.com/webtoon/list?titleId={titleId}&page={page}&sort=DESC'
            driver.get(base_url)
            time.sleep(0.01)  # 페이지 로딩 대기, 삭제 또는 변경 가능성 있음

            for i in range(1, 21):  # 한 페이지에 20개의 에피소드 가정
                try:
                    episode_xpath = f'/html/body/div[1]/div/div[2]/div/div[1]/div[3]/ul/li[{i}]/a'
                    episode_link = driver.find_element(By.XPATH, episode_xpath)
                    episode_number = episode_link.get_attribute('href').split('no=')[1].split('&')[0]
                    star_rating = driver.find_element(By.XPATH,
                                                      f'/html/body/div[1]/div/div[2]/div/div[1]/div[3]/ul/li[{i}]/a/div[2]/div/span[1]/span').text
                    ratings.append({'episode': int(episode_number), 'star': float(star_rating)})
                    last_episode = max(last_episode, int(episode_number))
                except NoSuchElementException:
                    break
                except Exception as e:
                    print(f"Error fetching rating for episode {i} on page {page}: {str(e)}")
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

    # TODO def create_stars(s_list) <- 매개변수를 너무나도 잘못이해..., 다시 확인 바람. db 코드에는 return값이 id가 아니므로 이 부분은 변경해도 됨.
    record_id = db.create_stars({'titleId': titleId, 'ratings': ratings})
    return record_id, last_episode

if __name__ == "__main__":  ##usecase 에서 실행 할 수 있도록 수정 예정!
    title_id = 764480  # 예시 웹툰 ID
    ratings, last_episode = star_crawler(title_id)  # 별점 크롤링시 활성화
    print(f"Last crawled episode: {last_episode}")  # 별점 크롤링시 활성화
    print("Ratings:", ratings)  # 별점 크롤링시 활성화

    #comments = comments_crawler(title_id, 50, 52)  # 50화부터 52화까지의 댓글을 크롤링, 댓글 크롤링 테스트시 활성화
    #print("Crawling completed. Comments collected from episodes 50 to 52.") #댓글 크롤링 테스트시 활성화