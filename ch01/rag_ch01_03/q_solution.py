# -*- coding: utf-8 -*-
# 1장 3강 퀴즈: 다른 질문의 입력 만들기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 chunks, retrieve, build_context를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

def prepare_input(question, chunks, k=2):
    # k는 검색 후보 수이고 max_chars는 그 후보를 Context에 넣는 예산이에요.
    # 검색된 모든 후보가 모델 입력에 들어간다고 가정하지 말고 두 결과를 구분해요.
    rows = retrieve(question, chunks, method="bm25", k=k)
    context, sources = build_context(rows, max_chars=260)
    return {"question": question, "context": context, "sources": sources}


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
new_question = "재택근무는 주 몇 회인가요?"
result = prepare_input(new_question, chunks)
for row in retrieve(new_question, chunks, method="bm25", k=2):
    print("후보:", row["document_id"], row["text"])
print("질문:", result["question"])
print("Context:", result["context"])
print("출처:", [(s["id"], s["document_id"]) for s in result["sources"]])

assert set(result) == {"question", "context", "sources"}
assert result["question"] == new_question
assert [(s["id"], s["document_id"]) for s in result["sources"]] == [("S1", "remote")]
assert "주 2회" in result["context"] and "일정 협의" in result["context"]
assert len(result["context"]) <= 260
print("\n✅ 정답이에요!")
print("생각해 보기:", "k=2로 요청했는데 출처가 하나뿐인 이유를 검색 점수로 설명해 보세요. 협업 시간 문장이 끊긴 점도 확인해요.")
