"""각 강의 prepare.py로 만든 vectors.npy를 메모리 Qdrant에 등록하는 도우미."""
from uuid import NAMESPACE_URL, uuid5
from qdrant_client import QdrantClient, models
from embedding_io import load_chunks, load_vectors, load_model


# 강의 폴더에 저장된 벡터로 Qdrant 색인을 만드는 도우미예요.
# 문서 벡터는 재사용하고 질문을 검색할 때만 질문 임베딩을 계산해요.
class SavedDenseIndex:
    def __init__(self, chunks, vectors, model):
        self.chunks, self.model = chunks, model
        # 메모리 Collection의 벡터 차원을 저장 파일에 맞춰 생성해요.
        # 각 청크의 본문과 출처를 payload에 넣어 검색 후 다시 원문을 찾을 수 있게 해요.
        self.client = QdrantClient(":memory:")
        self.collection = "campus_saved_e5"
        self.client.create_collection(self.collection, vectors_config=models.VectorParams(
            size=int(vectors.shape[1]), distance=models.Distance.COSINE))
        # zip은 청크와 벡터를 같은 행 위치로 묶어요.
        # open_saved_index에서 먼저 지문과 행 수를 검사한 자료를 전달해요.
        points = [models.PointStruct(id=str(uuid5(NAMESPACE_URL, c["chunk_id"])),
                    vector=v.tolist(), payload=c) for c, v in zip(chunks, vectors)]
        self.client.upsert(self.collection, points=points, wait=True)

    # 질문과 k를 검사한 뒤 E5 query 임베딩을 만들어요.
    # current_only=False는 과거 규정까지 포함하는 비교 실험에서 사용해요.
    def search(self, question, k=5, category=None, current_only=True):
        if not question.strip() or k < 1:
            raise ValueError("질문은 비어 있지 않아야 하고 k는 1 이상이어야 합니다.")
        query = self.model.encode("query: " + question, normalize_embeddings=True)
        # must에 들어간 조건은 모두 만족해야 해요.
        # 현재 상태와 범주를 동시에 지정하면 해당 범주의 현재 규정 안에서만 검색해요.
        must = []
        if current_only:
            must.append(models.FieldCondition(key="metadata.status",
                match=models.MatchValue(value="current")))
        if category:
            must.append(models.FieldCondition(key="metadata.category",
                match=models.MatchValue(value=category)))
        # 필터를 만족하는 후보 중 상위 k개를 받아 payload와 점수를 일반 딕셔너리로 바꿔요.
        # 결과가 k개보다 적거나 빈 목록일 수 있다는 점을 호출한 쪽에서 고려해야 해요.
        hits = self.client.query_points(self.collection, query=query.tolist(), limit=k,
            query_filter=models.Filter(must=must) if must else None,
            with_payload=True).points
        return [{**p.payload, "score": float(p.score)} for p in hits]

    def close(self):
        self.client.close()


# 자료 읽기, 벡터 검증, 모델 로딩을 한 진입점으로 묶어요.
# 새로 열린 색인은 사용 뒤 close를 호출해 정리해야 해요.
def open_saved_index():
    chunks = load_chunks()
    return SavedDenseIndex(chunks, load_vectors(chunks), load_model())
