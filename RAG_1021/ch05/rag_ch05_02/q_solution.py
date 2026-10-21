# -*- coding: utf-8 -*-
# 5장 2강 퀴즈: k를 바꾸고 필요한 내용 찾기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 points, model, current_filter를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 준비: main.py 끝에서 client를 닫았으므로 같은 Collection에 28개 Point를 다시 등록해요.
client = QdrantClient(":memory:")
client.create_collection(collection, vectors_config=models.VectorParams(
    size=int(vectors.shape[1]), distance=models.Distance.COSINE))
client.upsert(collection, points=points, wait=True)

# k를 1과 3으로 바꾸며 현재 규정만 검색해요.
question2 = "출장 식비와 숙박비의 한도는 각각 얼마이고 두 한도를 합쳐 쓸 수 있나요?"
query2 = model.encode("query: " + question2, normalize_embeddings=True)
results = {}
for k in [1, 3]:
    found = client.query_points(
        collection, query=query2.tolist(), limit=k,
        query_filter=current_filter, with_payload=True,
    ).points
    results[k] = [(hit.payload["document_id"], hit.payload["start"]) for hit in found]
    print("k", k)
    for hit in found:
        print(hit.paylaod["document_id"], hit.payload["text"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("k=1:", results[1], "| k=3:", results[3])
assert results[1] == [("meal", 60)], "k=1이면 합산 금지 문장(meal:60) 하나뿐이에요"
assert results[3] == [("meal", 60), ("meal", 0), ("travel", 0)]
assert all(doc != "travel-old" for doc, _ in results[3]), "current_filter를 넣었는지 확인하세요"
client.close()
print("\n✅ 정답이에요!")
print("생각해 보기:", "식비 금액, 숙박비 금액, 합산 가능 여부가 각각 어느 결과 문장에 있는지 표로 정리하고, 이번 질문에 고를 k와 그 이유를 적어 보세요.")
