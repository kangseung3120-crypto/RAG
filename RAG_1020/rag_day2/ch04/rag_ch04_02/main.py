"""4장 2강: 손계산에서 실제 검색으로."""
import numpy as np
from embedding_io import load_chunks, load_vectors, load_model, exact_rows, show_rows

# %% 1. 내적과 코사인
# 방향이 같은 벡터, 수직인 벡터, 반대 방향 벡터를 손계산용으로 준비해요.
# 내적은 길이의 영향을 받지만 코사인은 두 벡터의 길이로 나누어 방향을 비교해요.
q = np.array([3., 4.])
candidates = np.array([[6., 8.], [4., -3.], [-3., -4.]])
dots = candidates @ q  # vactors @ query
cosines = dots / (np.linalg.norm(candidates, axis=1) * np.linalg.norm(q))
print("[1] 내적", dots.tolist(), "코사인", cosines.tolist())
print("q norm", np.linalg.norm(q), "candidate norms", np.linalg.norm(candidates, axis=1).tolist())

# %% 2. 실제 E5 검색
# 청크와 저장 벡터의 대응 관계를 검사한 뒤 같은 E5 모델로 질문을 변환해요.
chunks = load_chunks()
vectors = load_vectors(chunks)
model = load_model()
question = "출장 숙박 비용 한도와 필요한 증빙은?"
# vectors가 청크 수 × 384, query가 384라면 scores는 청크 수만큼의 1차원 배열이에요.
# 각 점수가 어느 청크의 값인지 행 순서를 유지해야 해요.
query = model.encode("query: " + question, normalize_embeddings=True)
scores = vectors @ query
print("[2] scores shape", scores.shape)
show_rows(exact_rows(question, chunks, vectors, model, k=4))

# %% 3. 정답이 없는 질문도 순위가 나옵니다
print("[3] 정답 없는 질문")
# 자료에 정답이 없어도 가장 비슷한 후보는 나와요.
# 유사도 상위 결과가 존재한다는 사실만으로 답변 가능하다고 판단하면 안 돼요.
show_rows(exact_rows("회사의 올해 매출 목표는 얼마인가요?", chunks, vectors, model, k=2))
