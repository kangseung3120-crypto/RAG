"""4장 3강: 동일 질문에서 k와 임계값 비교."""
from embedding_io import load_chunks, load_vectors, load_model, exact_rows, show_rows

# 질문에 필요한 정답 문서는 식비 규정과 숙박비 규정 두 개예요.
# gold는 검색기가 참고하는 입력이 아니라 결과를 채점할 때만 사용하는 기준이에요.
chunks = load_chunks()
vectors = load_vectors(chunks)
model = load_model()
question = "출장 식비와 숙박비의 한도는 각각 얼마이고 두 한도를 합쳐 쓸 수 있나요?"
gold = {"meal", "travel"}

# %% 1. k 비교
# k를 늘리며 정답 문서 회수율과 Context로 보낼 문자 수를 함께 비교해요.
# 같은 문서의 청크가 여러 개 나와도 found는 set이므로 문서 한 개로 계산해요.
for k in [1, 2, 3, 5]:
    rows = exact_rows(question, chunks, vectors, model, k=k)
    found = {r["document_id"] for r in rows}
    print("[1]", k, sorted(found), "recall", len(gold & found) / len(gold),
          "chars", sum(len(r["text"]) for r in rows))
show_rows(exact_rows(question, chunks, vectors, model, k=5))

# %% 2. 임계값 비교
# 임계값을 높이면 낮은 점수의 후보가 줄지만 필요한 근거도 사라질 수 있어요.
# 아래 수치는 이 모델과 자료의 비교용이며 다른 모델에 그대로 적용할 기준은 아니에요.
for threshold in [None, .80, .84, .88]:
    rows = exact_rows(question, chunks, vectors, model, k=5, threshold=threshold)
    print("[2]", threshold, len(rows), [r["document_id"] for r in rows])

# %% 3. 두 질문의 점수 범위
# 답이 있는 질문과 없는 질문의 점수 범위가 겹치는지 살펴봐요.
# 점수 하나만으로 답변 보류를 결정하기 어려운 이유를 확인하는 단계예요.
for q in [question, "회사의 올해 매출 목표는 얼마인가요?"]:
    rows = exact_rows(q, chunks, vectors, model, k=3)
    print("[3]", q, [round(r["score"], 4) for r in rows])
