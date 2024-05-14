from db import get_one_webtoons
from positive_nlp import emotion_nlp
from similarity_nlp import similarity_nlp
from toon_crawler import comments_crawler, star_crawler

#0514 임시 크롤링 실행
def execute_crawling(title_id):
    comments = comments_crawler(title_id, 1, 3)
    record_id, last_episode = star_crawler(title_id)  # 별점 크롤링시 마지막 에피소드 정보 반환
    print("Crawling completed.")
    print("Record ID:", record_id)
    print("Last episode crawled:", last_episode)
    print("Comments collected:", comments)

def analysis_Usecase(tit):
    # '764480', 95 예시
    titleID = '764480'
    lastep = 95

    # # get_one_webtoons 함수에서 웹툰 record_id 받아오기
    # webtoon = get_one_webtoons(tit)
    # record_id = webtoon['id']
    # url = webtoon['url']
    # titleID 따로 추출하거나 크롤러에서 받아올 예정

    # # 두 크롤러가 쓰레드로 실행
    # # 댓글 크롤러
    # comments_crawler(url)
    #
    # # 별점 크롤러
    # stars_crawler(url)
    #
    # #별점 크롤러 실행 이후
    # star_id, last_ep = stars_usecase(title_id, record_id)

    # 유사성 모델 실행 확인 완료
    similarity_nlp(titleID, lastep)

    # 자연어 처리 모델 실행, 긍/부정 분류
    p_count, n_count = emotion_nlp(titleID, lastep)
    # 전체 긍/부정 DB에 저장

    # # 자연어 처리 모델 실행, 라벨링
    # labeling_nlp(title_id)
    #
    # # AI 호출해서 라벨링 된 데이터에서 피드백 요약
    # feedback_usecase(title_id, record_id)

    return True

# 아래로는 아직 검증 미완 --------------------------------------
# def feedback_usecase(title_id, record_id):
#     # title_id 의 txt 파일을 읽어와서 Ai로부터 피드백 받음(p_summary)
#
#     # 각 라벨별 댓글 갯수 파악 (p_count)
#
#     # 각 라벨에 대한 라벨 db 생성 (4개)
#     label_id = create_label(label, p_count, p_summary)
#     # 생성된 라벨을 해당 웹툰에 연결
#     update_label_webtoon(record_id, label_id)
#
#     return True
#
# def stars_usecase(title_id, record_id):
#     # title_id 의 txt 파일을 읽어와서 stars_list JSON 생성
#
#     # 별점 db 생성
#     star_id = create_stars(s_list)
#
#     # 생성된 별점 db를 해당 웹툰에 연결
#     update_stars_webtoon(record_id, star_id)
#
#     return True
#
# def total_feedback_usecase(record_id):
#     # record_id 값을 매개변수로 받아서 db에서 각 라벨의 p_summary 가져오기
#
#     # p_summary를 AI에 보내서 총평 피드백 생성
#     total_feedback = ""
#
#     return total_feedback