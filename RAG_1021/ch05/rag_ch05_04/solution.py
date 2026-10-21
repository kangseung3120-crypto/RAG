from rag_core import read_documents, chunk_documents
from embedding_io import load_chunks, load_vectors

# 같은 출장 원문을 새 청크 크기로 다시 나누어 갱신 상황을 만들어요.
# 본문이 같아도 청킹 조건이 바뀌면 chunk_id와 벡터를 다시 만들어야 해요.
chunks = load_chunks()
vectors = load_vectors(chunks)
travel = next(d for d in read_documents("documents.json")
              if d["document_id"] == "travel")
old = [c for c in chunks if c["document_id"] == "travel"]
new = chunk_documents([travel], size=100, overlap=20)
print([(c["start"], c["end"]) for c in old])
print([(c["start"], c["end"]) for c in new])

from uuid import NAMESPACE_URL, uuid5

# 옛 ID 집합에서 새 ID 집합을 빼면 더 이상 쓰지 않을 Point ID가 남아요.
# 새 ID까지 삭제하지 않도록 차집합의 방향을 확인하세요.
old_ids = {str(uuid5(NAMESPACE_URL, c["chunk_id"])) for c in old}
new_ids = {str(uuid5(NAMESPACE_URL, c["chunk_id"])) for c in new}
stale_ids = old_ids - new_ids
print(len(old_ids), len(new_ids), len(stale_ids))

from embedding_io import load_model

# 새 청크 본문을 같은 E5 모델로 다시 임베딩해요.
# 옛 청크 벡터를 길이만 맞춰 재활용하면 실제 본문과 검색 벡터가 어긋나요.
model = load_model()
new_vectors = model.encode(
    ["passage: " + c["text"] for c in new],
    normalize_embeddings=True,
)
print(new_vectors.shape)

from qdrant_client import QdrantClient, models

# 이 실습은 메모리 Collection에 출장 문서만 등록해 갱신 전후를 비교해요.
# 384는 현재 사용하는 E5 small의 차원이에요.
client = QdrantClient(":memory:")
client.create_collection("refresh_demo",
    vectors_config=models.VectorParams(
        size=384, distance=models.Distance.COSINE))
old_points = [
    models.PointStruct(
        id=str(uuid5(NAMESPACE_URL, c["chunk_id"])),
        vector=v.tolist(), payload=c)
    for c, v in zip(chunks, vectors)
    if c["document_id"] == "travel"
]
client.upsert("refresh_demo", points=old_points, wait=True)
print(client.count("refresh_demo").count)

# 새 Point를 먼저 Upsert해요. ID가 달라졌기 때문에 이 시점에는 옛 Point도 남아 있어 개수가 늘어요.
new_points = [
    models.PointStruct(
        id=str(uuid5(NAMESPACE_URL, c["chunk_id"])),
        vector=v.tolist(), payload=c)
    for c, v in zip(new, new_vectors)
]
client.upsert("refresh_demo", points=new_points, wait=True)
print(client.count("refresh_demo").count)

# stale_ids에 있는 옛 Point만 삭제한 뒤 새 청크 수와 같은지 확인해요.
# 이 예제의 Upsert와 Delete는 별도 동작이므로 운영 환경에서는 갱신 중 조회 일관성도 설계해야 해요.
client.delete(
    "refresh_demo",
    points_selector=models.PointIdsList(points=sorted(stale_ids)),
    wait=True,
)
print(client.count("refresh_demo").count)

import numpy as np

# 이 배열은 ANN에서 후보 일부만 탐색했을 때 정답을 놓칠 수 있음을 보여 주는 가상 점수예요.
# Qdrant 서버의 HNSW 성능을 측정한 결과가 아니에요.
scores = np.array([0.95, 0.93, 0.87, 0.55, 0.20])
exact = set(np.argsort(-scores)[:2].tolist())
# visited에 있는 후보만 비교해 상위 두 개를 고르고 전체 정확 검색의 상위 두 개와 겹침을 계산해요.
visited = np.array([0, 2, 4])
approx = set(visited[np.argsort(-scores[visited])[:2]].tolist())
print(sorted(exact), sorted(approx))
print(len(exact & approx) / 2)

# 삭제 집합에 새 Point가 섞이지 않았는지 확인하고, 탐색 후보를 넓혔을 때 상위 결과가 복원되는지 비교해요.
to_remove = old_ids - new_ids
print("삭제 대상 수:", len(to_remove))
print("새 ID를 삭제하는가:", bool(to_remove & new_ids))
assert len(to_remove)==3 and not to_remove & new_ids
visited = np.array([0, 1, 2, 4])
approx = set(visited[np.argsort(-scores[visited])[:2]].tolist())
print("확장 탐색:", sorted(approx), len(exact & approx)/2)


client.close()
