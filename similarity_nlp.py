from sentence_transformers import SentenceTransformer, util
import torch
import os

# Sentence BERT 모델 로드
embedder = SentenceTransformer("jhgan/ko-sroberta-multitask")

#TODO [Refactor] 중복 코드들을 하나의 함수에서 작동할 수 있도록 개선
def process_episode_comments(titleID, episode):
    comments_folder = os.path.join(os.getcwd(),  f'Webtoon_similarity_nlp_{titleID}')
    os.makedirs(comments_folder, exist_ok=True)
    cleaned_file_path = os.path.join(comments_folder, f'similarity_comments_{titleID}_{episode}.txt')

    file_path = f'Webtoon_{titleID}/comments_{titleID}_{episode}.txt'

    if not os.path.exists(file_path):
        print(f"{episode}화 댓글 파일이 존재하지 않습니다.")
        return

    with open(file_path, encoding='utf-8') as f:
        corpus = [line.strip() for line in f.readlines() if line.strip()]

    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    similarity_matrix = util.pytorch_cos_sim(corpus_embeddings, corpus_embeddings)

    cleaned_corpus = []
    checked_indices = set()

    for i in range(len(corpus)):
        if i in checked_indices:
            continue

        similar_indices = torch.where(similarity_matrix[i] >= 0.6)[0]
        duplicates = [idx.item() for idx in similar_indices if idx != i]

        if duplicates:
            checked_indices.update(duplicates)

        cleaned_corpus.append(corpus[i])
        checked_indices.add(i)

    with open(cleaned_file_path, "w", encoding='utf-8') as f:
        f.writelines([line + '\n' for line in cleaned_corpus])

    print(f"{episode}화 처리 완료, 처리된 문장 수: {len(cleaned_corpus)}")

def process_total_comments(titleID):
    comments_folder = os.path.join(os.getcwd(), f'Webtoon_similarity_nlp_{titleID}')
    final_file_path = os.path.join(comments_folder, f'final_similarity_removed_comments_{titleID}.txt')

    # comments_folder 내의 모든 파일을 읽습니다.
    episodes_files = [file for file in os.listdir(comments_folder) if file.startswith(f'similarity_comments_{titleID}_')]

    all_cleaned_corpus = []

    for episode_file in episodes_files:
        episode_file_path = os.path.join(comments_folder, episode_file)

        with open(episode_file_path, encoding='utf-8') as f:
            corpus = [line.strip() for line in f.readlines() if line.strip()]

        all_cleaned_corpus.extend(corpus)

    # 모든 에피소드에서 읽은 댓글에 대해 중복 제거를 위한 유사도 계산
    corpus_embeddings = embedder.encode(all_cleaned_corpus, convert_to_tensor=True)
    similarity_matrix = util.pytorch_cos_sim(corpus_embeddings, corpus_embeddings)

    final_cleaned_corpus = []
    checked_indices = set()

    for i in range(len(all_cleaned_corpus)):
        if i in checked_indices:
            continue

        similar_indices = torch.where(similarity_matrix[i] >= 0.6)[0]
        duplicates = [idx.item() for idx in similar_indices if idx != i]

        if duplicates:
            checked_indices.update(duplicates)

        final_cleaned_corpus.append(all_cleaned_corpus[i])
        checked_indices.add(i)

    # 최종 파일에 유사성이 제거된 댓글들을 저장
    with open(final_file_path, "w", encoding='utf-8') as f:
        f.writelines([line + '\n' for line in final_cleaned_corpus])

    print(f"최종 파일 처리 완료, 처리된 문장 수: {len(final_cleaned_corpus)}")

def similarity_nlp(titleID, lastep):
    for episode in range(1, lastep + 1):
        process_episode_comments(titleID, episode)

