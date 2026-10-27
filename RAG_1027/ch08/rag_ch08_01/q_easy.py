# -*- coding: utf-8 -*-
# 8장 1강 퀴즈: q09의 참고 답변을 근거 원문과 대조하기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 golden, by_id를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 질문 ID에 맞는 평가 항목을 고르고, 그 항목의 근거 문서를 원문으로 읽어요.
# 참고 답변의 금액, 횟수, 단위가 원문에 그대로 있는지 확인하세요.
target_id = "q09"
target = next(g for g in golden if g["question_ids"] == target_id) 
for did in target["relevant_document_ids"]:
    source = by_id[did]
    print(source["metadata"]["title"])
    print(source["content"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("질문:", target["question"])
print("참고 답변:", target["reference"])
assert target["question_id"] == "q09" and target["relevant_document_ids"] == ["education"]
assert source["document_id"] == "education", "q09의 근거 원문은 education이에요"
assert "분기 1회" in source["content"] and "30만원" in source["content"], "금액과 횟수를 함께 확인해요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "q05를 골라 참고 답변을 가린 채 원문만 읽고 필요한 사실 2~3개를 적은 뒤, 참고 답변과 비교해 보세요.")
