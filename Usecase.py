import db
from toon_crawler import comments_crawler, star_crawler

def analysis_Usecase(tit):
    # get_one_webtoons 함수에서 웹툰 record_id 받아오기
    webtoon = get_one_webtoons(tit)
    record_id = webtoon['id']  # 웹툰 DB와 연결한 record_id
    url = webtoon['url']

    # 두 크롤러가 쓰레드로 실행
    # 댓글 크롤러
    comments_crawler(url)
    # 별점 크롤러
    # 내부에서 별점 콜렉션안에 record 생성하고 그 record의 id값을 반환
    star_id, last_ep = stars_crawler(url)

    #별점 크롤러 실행 이후, 웹툰 DB에 연동하는 코드 (post)
    stars_usecase(title_id, record_id)

    return True
