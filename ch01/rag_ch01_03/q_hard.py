# -*- coding: utf-8 -*-
# 1장 3강 퀴즈: 다른 질문의 입력 만들기 (Hard: 교안의 TODO를 직접 완성해요)
# 이 폴더에서 uv run q_hard.py로 실행해요.
# main.py를 먼저 실행해 chunks, retrieve, build_context를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 검색 후보와 모델 입력을 만드는 두 단계를 함수로 묶어 보세요.
# 반환할 딕셔너리에는 원질문, 실제 Context, 그 Context의 출처가 함께 있어야 해요.
def prepare_input(question, chunks, k=2):
    # TODO 1: BM25로 검색 후보를 가져오세요.
    rows = retrieve(question, chunks, method="bm25", k=2)
    # TODO 2: 260자 예산으로 Context와 출처를 만드세요.
    context, sources = build_context(rows, max_chars=260)
    # TODO 3: question, context, sources가 있는 dict를 반환하세요.
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
