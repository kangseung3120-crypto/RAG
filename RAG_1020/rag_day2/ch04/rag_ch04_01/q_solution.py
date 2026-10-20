# -*- coding: utf-8 -*-
# 4장 1강 퀴즈: 질문도 같은 공간으로 옮기기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 model, np를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 질문은 검색을 요청하는 입력이므로 query: 접두사를 붙이고, 문서와 같은 조건으로 정규화해요.
question = "출장 호텔비는 얼마까지인가요?"
query_vector = model.encode(
    "query: " + question,
    normalize_embeddings=True,
)   
print(query_vector.shape)
print(round(float(np.linalg.norm(query_vector)), 6))


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert query_vector.shape == (384,), "질문 벡터는 384차원 1개예요"
assert abs(float(np.linalg.norm(query_vector)) - 1.0) < 1e-5, "normalize_embeddings=True로 길이를 1로 맞춰요"
expected = model.encode("query: " + question, normalize_embeddings=True)
assert np.allclose(query_vector, expected, atol=1e-5), "질문에는 passage: 가 아니라 query: 접두사를 붙여요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "질문에 passage:를 붙여도 실행은 돼요. 그래도 query:를 써야 하는 이유를 E5의 학습 방식으로 설명해 보세요.")
