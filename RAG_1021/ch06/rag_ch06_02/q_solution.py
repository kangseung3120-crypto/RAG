# -*- coding: utf-8 -*-
# 6장 2강 퀴즈: 질문을 두 문서가 필요한 경우로 바꾸기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 prepare를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 준비: main.py 끝에서 index를 닫았으므로 저장된 색인을 다시 열어요.
index = open_saved_index()

# 같은 복합 질문에서 k만 바꿔 근거 범위를 비교해요.
question = "출장 식비와 숙박비의 한도는 각각 얼마이고 두 한도를 합쳐 쓸 수 있나요?"
results, contexts = {}, {}
for k in [1, 3]:
    state = prepare(index, {"question": question, "k": k})
    document_ids = {s["document_id"] for s in state["sources"]}
    results[k], contexts[k] = sorted(document_ids), state["context"]
    print(k, results[k])
    print(state["context"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert results[1] == ["meal"] and results[3] == ["meal", "travel"]
assert "12만원" not in contexts[1] and "3만원" not in contexts[1], "k=1 Context에는 두 금액이 없어요"
assert all(t in contexts[3] for t in ["1일 3만원", "1박당 12만원", "합산하지 않습니다"])
index.close()
print("\n✅ 정답이에요!")
print("생각해 보기:", "Ollama가 준비됐다면 k=1과 k=3으로 실제 답변을 생성해, k=1에서 모델이 숙박 금액을 추측하는지 확인해 보세요.")
