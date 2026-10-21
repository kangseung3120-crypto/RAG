from embedding_io import load_chunks, load_vectors

# 청크 목록과 임베딩 행렬은 같은 순서여야 해요.
# travel 청크의 위치 number를 찾고 그 위치의 벡터를 짝지어 하나의 Point를 만들어요.
chunks = load_chunks()
vectors = load_vectors(chunks)
number = next(i for i, c in enumerate(chunks)
              if c["document_id"] == "travel")
chunk = chunks[number]
vector = vectors[number]
print(number, chunk["document_id"], chunk["start"], chunk["end"])
print(len(vector), chunk["metadata"]["title"])

print(chunk["text"])
print(sorted(chunk))

from uuid import NAMESPACE_URL, uuid5
from qdrant_client import models

# UUID5는 같은 chunk_id에 항상 같은 ID를 만들어요.
# Point는 식별자 id, 검색용 vector, 원문/출처를 담은 payload 세 부분으로 구성돼요.
point_id = str(uuid5(NAMESPACE_URL, chunk["chunk_id"]))
point = models.PointStruct(
    id=point_id,
    vector=vector.tolist(),
    payload=chunk,
)
print(point.id)
print(point_id == str(uuid5(NAMESPACE_URL, chunk["chunk_id"])))

from qdrant_client import QdrantClient

# 메모리 Qdrant는 별도 서버나 계정 없이 실행되며 종료하면 자료가 사라져요.
# Collection 차원은 실제 벡터의 열 수와 맞추고 비교 기준은 코사인으로 지정해요.
client = QdrantClient(":memory:")
client.create_collection(
    "point_demo",
    vectors_config=models.VectorParams(
        size=int(vectors.shape[1]),
        distance=models.Distance.COSINE,
    ),
)
print(client.count("point_demo").count)

# 같은 ID로 두 번 Upsert하면 새 Point 두 개가 아니라 기존 Point 하나를 갱신해요.
# 등록할 때마다 count를 출력해 중복 생성되지 않는지 확인해요.
for repeat in range(2):
    client.upsert("point_demo", points=[point], wait=True)
    print("등록", repeat + 1, "Point 수",
          client.count("point_demo").count)

# retrieve는 유사도 검색이 아니라 정확한 Point ID로 읽는 조회예요.
# with_payload=True로 저장한 원문 정보가 그대로 돌아오는지 확인해요.
saved = client.retrieve(
    "point_demo",
    ids=[point_id],
    
)[0]
print(saved.payload["document_id"])
print(saved.payload["metadata"]["title"])
print(saved.payload["start"], saved.payload["end"])

# TODO: 본문의 실습 코드를 이 줄 아래, 연결 종료 코드 위에 작성하세요.

# 이 아래에서는 메모리 색인을 사용할 수 없어요. 직접 해보는 실습은 close 위에 작성하세요.
client.close()
