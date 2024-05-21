import db
from labeling_nlp import labeling_nlp
from llm import total_feedback
from positive_nlp import emotion_nlp
from similarity_nlp import similarity_nlp
from urllib.parse import urlparse, parse_qs
from toon_crawler import comments_crawler, star_crawler
import logging

# 표준 Python 로깅 모듈 설정
logging.basicConfig(filename='analysis.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analysis_Usecase(tit):
    try:
        logging.info(f"Starting analysis for webtoon: {tit}")
        webtoon = db.get_one_webtoons(tit)
        record_id = webtoon['id']
        url = webtoon['url']
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        title_id = query_params.get('titleId', [None])[0]

        # 별점 크롤러 실행
        logging.info(f"Crawling stars for titleId {title_id}")
        star_id, last_ep = star_crawler(title_id)
        db.update_stars_webtoon(record_id, star_id, last_ep)
        logging.info(f"Star crawling completed for titleId {title_id}")

        # 댓글 크롤러 실행
        logging.info(f"Crawling comments for titleId {title_id}")
        comments_crawler(title_id, last_ep)
        logging.info(f"Comments crawling completed for titleId {title_id}")

        # 유사도 분석
        logging.info(f"Starting similarity analysis for titleId {title_id}")
        similarity_nlp(title_id, last_ep)
        logging.info(f"Similarity analysis completed for titleId {title_id}")

        # 긍정/부정 감성 분석
        logging.info(f"Starting emotion analysis for titleId {title_id}")
        p_count, n_count = emotion_nlp(title_id, last_ep)
        count_id = db.create_count(p_count, n_count)
        db.update_count_webtoon(record_id, count_id)
        logging.info(f"Emotion analysis completed for titleId {title_id}")

        # 자연어 처리 모델 실행, 라벨링
        logging.info(f"Starting labeling for titleId {title_id}")
        labeling_nlp(title_id, last_ep)
        logging.info(f"Labeling completed for titleId {title_id}")

        # 라벨 업데이트
        logging.info(f"Updating labels for titleId {title_id}")
        label_Update_Usecase(title_id, record_id)
        logging.info(f"Label update completed for titleId {title_id}")

        # AI 호출해서 라벨링 된 데이터에서 피드백 요약
        logging.info(f"Starting total feedback for titleId {title_id}")
        total_feedback(title_id, record_id)
        logging.info(f"Total feedback completed for titleId {title_id}")

        return True
    except Exception as e:
        logging.error(f"Error during analysis for webtoon {tit}: {e}")
        return False

def label_Update_Usecase(title_id, record_id):
    try:
        # 라벨
        label_names = {0: '작화', 1: '스토리', 2: '분량', 3: '기타'}

        # 라벨별 댓글 데이터 준비
        comments_by_label = {}
        with open(f'Webtoon_label_nlp/label_comments_{title_id}.txt', 'r', encoding='utf-8') as file:
            for line in file:
                comment, label = line.strip().split('\t')
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
            logging.info(f"Label ID: {label_id}, Label Name: {label_name}, Comment Count: {comment_count}")

        # 웹툰에 라벨 업데이트
        db.update_label_webtoon(record_id, label_ids)
        logging.info(f"Labels updated for record ID: {record_id}")

        return True
    except Exception as e:
        logging.error(f"Error during label update for titleId {title_id}: {e}")
        return False
