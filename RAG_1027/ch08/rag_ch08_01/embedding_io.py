"""각 강의 폴더의 청크와 임베딩 파일을 읽고 검색하는 보조 함수."""
import hashlib
import json
import os
from pathlib import Path
import numpy as np

MODEL_ID = "intfloat/multilingual-e5-small"


# 각 강의 폴더에 포함된 청크를 읽어요. 다른 강의 폴더에 의존하지 않아요.
def load_chunks():
    return json.loads(Path("chunks.json").read_text(encoding="utf-8"))


# 청크 ID와 본문을 순서대로 직렬화해 지문을 만들어요.
# 벡터의 i번째 행이 청크의 i번째 항목과 계속 대응하는지 확인하는 데 사용해요.
def fingerprint(chunks):
    text = json.dumps([(c["chunk_id"], c["text"]) for c in chunks], ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# 모델 추론은 CPU에서 수행해요. RAG_MODEL_CACHE를 지정하면 다운로드 캐시 위치를 바꿀 수 있어요.
def load_model(model_id=MODEL_ID):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_id, device="cpu",
        cache_folder=os.environ.get("RAG_MODEL_CACHE"))


def load_vectors(chunks):
    # 저장 당시의 청크 지문과 현재 지문이 다르면 이전 벡터를 그대로 쓰면 안 돼요.
    # 청크 순서가 바뀐 경우도 탐지해 잘못된 본문에 검색 점수를 연결하는 일을 막아요.
    config = json.loads(Path("embedding_config.json").read_text(encoding="utf-8"))
    if config["chunk_fingerprint"] != fingerprint(chunks):
        raise ValueError("chunks.json이 바뀌었습니다. 이 폴더의 임베딩 생성 코드를 다시 실행하세요.")
    # vectors의 행 수는 청크 수와 같아야 해요. 열 수는 모델의 임베딩 차원이에요.
    # 두 조건은 파일의 대응 관계를 확인하는 기본 검사예요.
    vectors = np.load("vectors.npy")
    if len(vectors) != len(chunks):
        raise ValueError("청크와 벡터의 행 수가 다릅니다.")
    return vectors


def exact_rows(question, chunks, vectors, model, k=5, threshold=None):
    # 문서와 동일한 모델로 질문을 임베딩하되 query 접두사를 써요.
    # 양쪽 벡터가 정규화되어 있으므로 행렬과 질문 벡터의 내적이 코사인 유사도가 돼요.
    query = model.encode("query: " + question, normalize_embeddings=True)
    scores = vectors @ query
    # 현재 규정만 검색 후보로 남긴 뒤 점수 내림차순으로 정렬해요.
    # 동점일 때는 chunk_id로 순서를 고정하고, 임계값을 통과한 후보 중 최대 k개를 반환해요.
    eligible = [i for i, c in enumerate(chunks)
                if c["metadata"]["status"] == "current"]
    order = sorted(eligible, key=lambda i: (-float(scores[i]), chunks[i]["chunk_id"]))
    return [{**chunks[i], "score": float(scores[i])} for i in order
            if threshold is None or scores[i] >= threshold][:k]


# 순위, 원문 ID, 시작 위치, 점수, 본문을 함께 출력해요.
# 같은 문서의 여러 청크가 나왔는지와 실제 질문의 근거가 있는지를 같이 확인하세요.
def show_rows(rows):
    for rank, row in enumerate(rows, 1):
        print(rank, row["document_id"], row["start"], f'{row["score"]:.4f}', row["text"])
