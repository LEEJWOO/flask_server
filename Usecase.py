import db
from toon_crawler import comments_crawler, star_crawler
from urllib.parse import urlparse, parse_qs

def analysis_Usecase(tit):
    # get_one_webtoons 함수에서 웹툰 record_id 받아오기
    webtoon = db.get_one_webtoons(tit)
    record_id = webtoon['id']  # 웹툰 DB와 연결한 record_id
    url = webtoon['url']

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    title_id = query_params.get('titleId', [None])[0]
    lastep = 3

    # 별점 크롤러
    # 내부에서 별점 콜렉션안에 record 생성하고 그 record의 id값을 반환
    star_id, last_ep = star_crawler(title_id)


    # 별점 크롤러 실행 이후, 웹툰 DB에 연동하는 코드 (post)
    db.update_stars_webtoon(record_id, star_id)
    # 두 크롤러가 쓰레드로 실행

    # 댓글 크롤러
    comments_crawler(title_id, last_ep)

    return True
