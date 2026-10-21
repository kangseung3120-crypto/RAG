# -*- coding: utf-8 -*-
# 5장 1강 퀴즈: 교육비 청크 한 개 추가하기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 chunks, vectors, point를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 준비: main.py 끝에서 client를 닫았으므로 같은 Collection(출장 Point 1개)을 다시 만들어요.
from qdrant_client import QdrantClient
client = QdrantClient(":memory:")
client.create_collection("point_demo", vectors_config=models.VectorParams(
    size=int(vectors.shape[1]), distance=models.Distance.COSINE))
client.upsert("point_demo", points=[point], wait=True)

# 교육 문서 청크의 ID와 같은 행의 벡터로 Point를 완성해요.
# 앞에서 만든 출장 Point와 서로 다른 ID가 되는지, 반복 등록하면 수가 유지되는지 확인하세요.
education_no = next(i for i, c in enumerate(chunks)
                    if c["document_id"] == "education")
education_chunk = chunks[education_no]
education_point = models.PointStruct(
    id=str(uuid5(NAMESPACE_URL, education_chunk["chunk_id"])),
    vector=vectors[education_no].tolist(),
    payload=education_chunk,
)

client.upsert("point_demo", points=[education_point], wait=True)
print(client.count("point_demo").count)

# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
import numpy as np
assert client.count("point_demo").count == 2, "출장 1개 + 교육비 1개 = 2개여야 해요"
client.upsert("point_demo", points=[education_point], wait=True)
print("한 번 더 등록:", client.count("point_demo").count)
assert client.count("point_demo").count == 2, "같은 ID로 다시 넣으면 수가 그대로예요"
saved = client.retrieve("point_demo", ids=[education_point.id], with_payload=True, with_vectors=True)[0]
print(saved.payload["metadata"]["title"], "|", saved.payload["text"][:30])
assert saved.payload["document_id"] == "education"
assert np.allclose(saved.vector, vectors[education_no], atol=1e-5), "교육비 본문에는 education_no 행의 벡터를 붙여야 해요"
client.close()
print("\n✅ 정답이에요!")
print("생각해 보기:", "출장 Point를 uuid5 대신 매번 새 UUID로 등록하면 무엇을 기준으로 중복이 판단될지, 같은 원문을 다시 수집할 때 필요한 ID 규칙을 한 문장으로 적어 보세요.")
