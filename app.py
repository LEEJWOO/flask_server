from flask import Flask, request, render_template
import db
import llm
from toon_crawler import comments_crawler
import asyncio
import sys
sys.path.append('C:\\flask_server\\kit452\\Scripts')
print(sys.path) #실행 경로 테스트용 임시

app = Flask(__name__)

#0430 유승우 코드 추가
@app.route('/')
def hello():  # put application's code here
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    comic_title = request.args.get('title', default='', type=str)
    return render_template('analysis.html', title=comic_title)

#TODO 폼에서 값을 받아와 읽는 API 루트 처리로 return에서 다시 main 화면으로 돌아가게 해야할 듯 함.
@app.route("/new_webtoon")
def new_webtoon():
    title = request.args.get('title')
    url = request.args.get('url')

    result = db.create_webtoon(title, url)
    return result

@app.route("/delete_webtoon")
def delete_webtoon():
    record_id = request.args.get('id')

    result = db.delete_webtoon(record_id)
    return result

#TODO 삭제 내부 동작으로만 실행됨
@app.route("/update_label_webtoon")
def update_label_webtoon():
    result = db.update_label_webtoon()
    return result

#TODO 삭제 내부 동작으로만 실행됨
@app.route("/update_stars_webtoon")
def update_stars_webtoon():
    result = db.update_stars_webtoon()
    return result

#TODO 삭제, 내부 동작으로만 실행됨
@app.route('/ai')
def ai_response():
    response = llm.generate_ai_response()
    return {"response": response}

#웹툰 목록
@app.route("/webtoons")
def webtoons():
    records = db.get_webtoons()
    return records

#TODO all 웹툰의 경우 label과 stars까지 출력하므로 아마 필요 없을 것 같음
@app.route("/webtoon_all")
def all_webtoon():
    result = db.get_all_webtoons()
    return result

#웹툰 1개
@app.route("/webtoon_one")
def one_webtoon():
    title = request.args.get('title')

    result = db.get_one_webtoons(title)
    return result



#TODO 매개변수 url(titleid), firstep, lastep(크롤러 내부 동작으로 얻어오기) 5/9
async def run_comments_crawler(titleId, start_episode, end_episode, week_day):
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, comments_crawler, titleId, start_episode, end_episode, week_day)
        return f"Crawling successfully completed. Result: {result}"
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route("/crawler")
async def crawler():
    titleId = request.args.get('titleId', type=int)  # url로부터 받아올 매개변수 titleId
    start_episode = request.args.get('startep', type=int)  # url로부터 받아올 매개변수 start_episode (삭제 예정)
    end_episode = request.args.get('lastep', type=int)  # url로부터 받아올 매개변수 end_episode (최신 회차 = 전체 회차 수)
    week_day = request.args.get('weekday', default='mon', type=str)  # url로부터 받아올 매개변수 week_day
    result = await run_comments_crawler(titleId, start_episode, end_episode, week_day)
    return f"Crawling completed. Result: {result}"
    print(result)

#TODO 별점 크롤러도 위와 동일하게 작업 5/9-10

#TODO 데이터라벨링을 위한 데이터 수집 5/10-5/11 오전 9시 : 바로 회의록 업로드

#TODO 삭제 내부 동작
@app.route('/create_label')
def create_label():
    label = "스토리"
    p_count = 35
    p_summary = "전개가 시원시원함"

    record = db.create_label(label, p_count, p_summary)

    return record

#TODO 삭제 내부 동작
@app.route('/create_stars')
def create_stars():

    s_list = [
        {"episode": 1, "star": 3.2},
        {"episode": 2, "star": 4.9},
        {"episode": 3, "star": 8.9},
        {"episode": 4, "star": 7.9},
        {"episode": 5, "star": 5.9},
        {"episode": 6, "star": 6.9}
    ]

    record = db.create_stars(s_list)

    return record

if __name__ == '__main__':
    app.run()
