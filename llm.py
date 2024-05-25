# -*- coding: utf-8 -*-
import google.generativeai as genai
import random
import db
import time

# 생성 설정 및 안전 설정 정의
generation_config = genai.GenerationConfig(
    candidate_count=1,  # 후보 개수 설정
    max_output_tokens=3000,  # 최대 출력 토큰 수 설정
    temperature=1.0,  # 온도 설정
    top_p=1.0,  # 상위 확률 합 설정
)

safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# 모델 초기화
model = genai.GenerativeModel(
    'gemini-1.0-pro-latest',
    safety_settings=safety_settings,
    generation_config=generation_config)


def load_and_prepare_data(title_id):
    comments_by_label = {}
    with open(f'Webtoon_label_nlp/label_comments_{title_id}.txt', 'r', encoding='utf-8') as file:
        for line in file:
            comment, label = line.strip().split('\t')
            if label in ['0', '1', '2', '3']:
                if label in comments_by_label:
                    comments_by_label[label].append(comment)
                else:
                    comments_by_label[label] = [comment]
    # 각 라벨별로 최대 40개 댓글 랜덤 선정
    selected_comments = {}
    for label, comments in comments_by_label.items():
        selected_comments[label] = random.sample(comments, min(len(comments), 40))
    return selected_comments


def label_feedback(title_id, retries=10, delay=40):
    attempt = 0
    while attempt < retries:
        try:
            selected_comments = load_and_prepare_data(title_id)
            input_text = """각 라벨별 댓글을 토대로 작가에게 요약 피드백을 제공할 거야. 너는 작가의 기분이 상하는 말은 전부 제외하고, 실제 댓글을 읽지 않고도 작가에게 도움이 될 만한 피드백을 해줘. 먼저 라벨별로 피드백을 최대 3줄 작성해줘. 주의! 작가에게 실제 댓글을 보라는 요청은 하지마. 필요하다면 특정 댓글을 정제해서 직접 전달해. 라벨은 0=작화, 1=스토리, 2=분량, 3=기타야.\n"""
            for label, comments in selected_comments.items():
                for comment in comments:
                    input_text += f"\"{comment}\", {label}\n"
            response = model.generate_content(input_text)
            return response.text
        except ValueError as e:
            print(f"ValueError 발생: {e}. 다시 시도합니다... (시도 {attempt + 1}/{retries})")
            attempt += 1
            time.sleep(delay)

    # 모든 재시도 실패 시 예외 발생
    raise Exception("모든 재시도에서 요청이 실패했습니다.")


def total_feedback(title_id, webtoon_id):
    label_summary = label_feedback(title_id)
    # AI로부터 생성된 라벨별 피드백을 이용하여 종합 피드백 생성
    input_text = "받은라벨별피드백을바탕으로작가에게전달할종합피드백을작성해줘.호평받아던사항과개선사항을알려주고,결론을적어줘.편지형식은쓰지마.\n" + label_summary
    total_response = model.generate_content(input_text)
    total_summary = total_response.text
    result = db.update_summary_webtoon(webtoon_id, label_summary, total_summary)
    return result