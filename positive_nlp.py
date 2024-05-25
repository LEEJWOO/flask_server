import os
import re
import json
import pickle
import tensorflow as tf
from konlpy.tag import Okt
import torch

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def clean_text(text):
    text = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', text)
    return text


def remove_stopwords(text, stopwords):
    okt = Okt()
    morphs = okt.morphs(text, stem=True)
    text = [word for word in morphs if not word in stopwords]
    return text


def load_model_and_tokenizer():
    with open('C:/flask_server/CLEAN_DATA/data_configs.json', 'r') as f:
        prepro_configs = json.load(f)

    with open('C:/flask_server/CLEAN_DATA/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    if isinstance(prepro_configs['vocab'], dict):
        tokenizer.word_index = prepro_configs['vocab']
        print("tokenizer에 설정 성공")
    else:
        print("prepro_configs['vocab']는 사전 형태가 아닙니다. tokenizer.word_index 설정 실패.")

    model = tf.keras.models.load_model('C:/flask_server/my_models/')

    return model, tokenizer


def emotion_nlp(titleID, lastep):
    # 불용어
    stopwords = ['은', '는', '이', '가', '하', '아', '것', '들', '의', '있', '되', '수', '보', '주', '등', '한']
    MAX_LENGTH = 8  # 문장최대길이

    # 모델 및 토크나이저 불러오기
    model, tokenizer = load_model_and_tokenizer()

    # 결과 저장 폴더 생성
    output_folder = f'Webtoon_emotion_nlp_{titleID}'
    os.makedirs(output_folder, exist_ok=True)

    positive_count = 0  # 긍정 댓글 개수
    negative_count = 0  # 부정 댓글 개수

    for ep in range(1, lastep + 1):
        file_path = f'Webtoon_similarity_nlp_{titleID}/similarity_comments_{titleID}_{ep}.txt'
        output_file_path = os.path.join(output_folder, f'emotion_comments_{titleID}_{ep}.txt')

        with open(file_path, 'r', encoding='utf-8') as f, open(output_file_path, 'w', encoding='utf-8') as wf:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                cleaned_line = clean_text(line)  # 텍스트 정제
                cleaned_line = remove_stopwords(cleaned_line, stopwords)  # 불용어 제거
                vector = tokenizer.texts_to_sequences([cleaned_line])

                # vector 내부 리스트의 각 원소에서 None 값을 제거
                vector = [[item for item in sublist if item is not None] for sublist in vector]
                pad_new = tf.keras.preprocessing.sequence.pad_sequences(vector, maxlen=MAX_LENGTH)  # 패딩

                predictions = model.predict(pad_new)
                predictions = float(predictions.squeeze(-1))

                # 긍정 댓글만 파일에 저장
                if predictions > 0.6:
                    positive_count += 1
                    wf.write(f'{line}\n')
                elif predictions < 0.4:
                    negative_count += 1

    # 긍정 댓글과 부정 댓글의 개수 반환
    return positive_count, negative_count