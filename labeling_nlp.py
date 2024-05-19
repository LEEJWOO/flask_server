import os
import re
import json
import pickle
import tensorflow as tf
from konlpy.tag import Okt
import numpy as np
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 단어와 라벨의 사전 정의
word_to_label = {
    '작화': 0, '그림체': 0, '선': 0, '채색': 0, '배경': 0, '디테일': 0, '색감': 0, '드로잉': 0, '일러스트': 0, '미국 그림체': 0,
    '수채화': 0, '실선': 0, '표현력': 0, '연출력': 0, '전투씬': 0, '탄탄': 0, '털선': 0, '마카': 0, '추상화': 0, '피카소': 0, '마커': 0, '액션씬': 0,
    '그리': 0, '그림': 0, '작풍': 0, '인체': 0, '곡선': 0, '인삐': 0,
    '소재': 1, '스토리': 1, '추측': 1, '내용': 1, '흥미진진': 1, '소름': 1, '재미': 1, '이해': 1, '떡밥': 1, '에피소드': 1, '스케일': 1, '이야기': 1,
    '세계관': 1, '진행': 1, '구상': 1, '빅피쳐': 1, '추리': 1, '전개': 1, '분량': 2, '쿠키': 3, '이모티콘': 3, '스포': 3,
}

# 불용어
stop_words_path = 'C:/flask_server/DATA/stopword.txt'  # stop_words 파일 경로 설정
with open(stop_words_path, 'r', encoding='utf-8') as f:
    stopwords = [word.strip() for word in f.readlines()]
MAX_LENGTH = 20  # 문장최대길이


def clean_text(text):
    text = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', text)
    return text


def remove_stopwords(text, stopwords):
    okt = Okt()
    morphs = okt.morphs(text, stem=True)
    text = [word for word in morphs if not word in stopwords]
    return text


def load_model_and_tokenizer():
    with open('C:/flask_server/CLEAN_DATA_TOON/data_configs.json', 'r') as f:
        prepro_configs = json.load(f)

    with open('C:/flask_server/CLEAN_DATA_TOON/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    if isinstance(prepro_configs['vocab'], dict):
        tokenizer.word_index = prepro_configs['vocab']
        print("tokenizer에 설정 성공")
    else:
        print("prepro_configs['vocab']는 사전 형태가 아닙니다. tokenizer.word_index 설정 실패.")

    model = tf.keras.models.load_model('C:/flask_server/my_toon_models/')

    return model, tokenizer


def predict_label(line, model, tokenizer):
    words = line.split()  # 댓글을 단어 단위로 분리
    cleaned_line = clean_text(line)
    cleaned_line = remove_stopwords(cleaned_line, stopwords)
    for word in cleaned_line:
        if word in word_to_label:
            return word_to_label[word]  # 사전에 정의된 라벨 반환
    vector = tokenizer.texts_to_sequences([cleaned_line])
    pad_new = tf.keras.preprocessing.sequence.pad_sequences(vector, maxlen=MAX_LENGTH)
    predictions = model.predict(pad_new)
    label = np.argmax(predictions)

    return label


def labeling_nlp(title_id, lastep):
    comments_folder = os.path.join(os.getcwd(), 'Webtoon_label_nlp')
    os.makedirs(comments_folder, exist_ok=True)
    cleaned_file_path = os.path.join(comments_folder, f'label_comments_{title_id}.txt')

    # 모델 및 토크나이저 불러오기
    model, tokenizer = load_model_and_tokenizer()

    with open(cleaned_file_path, 'w', encoding='utf-8') as wf:
        for episode in range(1, lastep + 1):
            file_path = f'Webtoon_emotion_nlp_{title_id}/emotion_comments_{title_id}_{episode}.txt'
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        label = predict_label(line, model, tokenizer)  # 라벨 예측
                        wf.write(f'{line}\t{label}\n')
            except FileNotFoundError:
                print(f'{file_path} 파일을 찾을 수 없습니다.')

