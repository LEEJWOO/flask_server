import db
from labeling_nlp import labeling_nlp
from llm import total_feedback
from positive_nlp import emotion_nlp
from similarity_nlp import similarity_nlp
from urllib.parse import urlparse, parse_qs
from toon_crawler import comments_crawler, star_crawler


def analysis_Usecase(tit):
    webtoon = db.get_one_webtoons(tit)
    record_id = webtoon['id']
    url = webtoon['url']
    latest_ep = webtoon['last_ep']
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    title_id = query_params.get('titleId', [None])[0]

    # 별점 크롤러
    star_id, last_ep = star_crawler(title_id)
    if latest_ep >= last_ep:
        db.delete_stars(star_id) #별점 크롤러로 만들어진 star 레코드 값을 연동 전에 삭제
        return True

    db.update_stars_webtoon(record_id, star_id, last_ep)

    # 댓글 크롤러
    comments_crawler(title_id, last_ep)

    similarity_nlp(title_id, last_ep)

    p_count, n_count = emotion_nlp(title_id, last_ep)
    count_id = db.create_count(p_count, n_count)
    db.update_count_webtoon(record_id, count_id)

    # 자연어 처리 모델 실행, 라벨링
    labeling_nlp(title_id, last_ep)

    label_Update_Usecase(title_id, record_id)

    # AI 호출해서 라벨링 된 데이터에서 피드백 요약
    total_feedback(title_id, record_id)

    return True


def label_Update_Usecase(title_id, record_id):
    # 라벨
    label_names = {0: '작화', 1: '스토리', 2: '분량', 3: '기타'}

    # 라벨별 댓글 데이터 준비
    comments_by_label = {}
    with open(f'Webtoon_label_nlp/label_comments_{title_id}.txt', 'r', encoding='utf-8') as file:
        for line in file:
            comment, label = line.strip().split('\t')
            # 라벨이 '4'일 경우 건너뛰기
            if label == '4':
                continue
            if label in comments_by_label:
                comments_by_label[label].append(comment)
            else:
                comments_by_label[label] = [comment]

    # 라벨별로 전체 댓글 수 세기
    comments_count_by_label = {label: len(comments) for label, comments in comments_by_label.items()}

    # 라벨 아이디들을 저장할 리스트 초기화
    label_ids = []

    for label, comment_count in comments_count_by_label.items():
        # 라벨 이름 가져오기
        label_name = label_names[int(label)]

        # 라벨 데이터 생성
        label_id = db.create_label(label_name, comment_count)
        label_ids.append(label_id)
        print(f"Label ID: {label_id}, Label Name: {label_name}, Comment Count: {comment_count}")

    # 웹툰에 라벨 업데이트
    db.update_label_webtoon(record_id, label_ids)

    return True