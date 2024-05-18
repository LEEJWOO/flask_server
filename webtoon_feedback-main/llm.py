import google.generativeai as genai
import random

# 생성 설정 및 안전 설정 정의
generation_config = genai.GenerationConfig(
    candidate_count=1,          # 후보 개수 설정
    max_output_tokens=3000,     # 최대 출력 토큰 수 설정
    temperature=1.0,            # 온도 설정
    top_p=1.0,                  # 상위 확률 합 설정
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
    safety_settings,
    generation_config)

def load_and_prepare_data(title_id):
    comments_by_label = {}
    with open(f'Webtoon_label_nlp/label_comments_{title_id}.txt', 'r', encoding='utf-8') as file:
        for line in file:
            comment, label = line.strip().split('\t')
            if label in comments_by_label:
                comments_by_label[label].append(comment)
            else:
                comments_by_label[label] = [comment]
    # 각 라벨별로 최대 40개 댓글 랜덤 선정
    selected_comments = {}
    for label, comments in comments_by_label.items():
        selected_comments[label] = random.sample(comments, min(len(comments), 40))
    return selected_comments

def label_feedback(title_id):
    selected_comments = load_and_prepare_data(title_id)
    input_text = """각 라벨별 댓글을 토대로 작가에게 요약 피드백을 제공할 거야. 너는 작가의 기분이 상하는 말은 전부 제외하고, 실제 댓글을 읽지 않고도 작가에게 도움이 될 만한 피드백을 해줘. 먼저 라벨별로 피드백을 작성해줘. 주의! 작가에게 실제 댓글을 보라는 요청은 하지마. 필요하다면 특정 댓글을 정제해서 직접 전달해. 라벨은 0=작화, 1=스토리, 2=분량, 3=기타야.\n"""
    for label, comments in selected_comments.items():
        for comment in comments:
            input_text += f"\"{comment}\", {label}\n"
    response = model.generate_content(input_text)
    return response.text
    
def total_feedback(title_id):
    ai_response = label_feedback(title_id)
    # AI로부터 생성된 라벨별 피드백을 이용하여 종합 피드백 생성
    input_text = "받은 라벨별 피드백을 바탕으로 작가에게 전달할 종합 피드백을 작성해줘:\n" + ai_response
    total_response = model.generate_content(input_text)
    return total_response.text