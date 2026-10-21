# -*- coding: utf-8 -*-
# 4장 4강 퀴즈: 모델 선택 이유를 결과로 설명하기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 report(small 결과), json, Path를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 질문 ID로 두 모델의 결과를 맞대어 검색 문서가 달라진 질문만 골라요.
recorded = json.loads(Path("recorded_e5_comparison.json").read_text(encoding="utf-8"))
candidate_report = recorded["intfloat/multilingual-e5-base"]["report"]
small_rows = {r["question_id"]: r for r in report["rows"]}
base_rows = {r["question_id"]: r for r in candidate_report["rows"]}
changed = []
for question_id, before in small_rows.items():
    after = base_rows[question_id]
    if before["retrieved_document_ids"] != after["retrieved_document_ids"]:
        changed.append(question_id)
        print(question_id, before["retrieved_document_ids"], after["retrieved_document_ids"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("달라진 질문:", changed)
assert changed == ['q04', 'q09', 'q10', 'q11', 'q12'], f"달라진 질문: {changed}"
assert candidate_report["hit_at_k"] == report["hit_at_k"] == 1.0, "두 모델 모두 Hit@3 = 1.0이에요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "결과가 다르다는 것만으로 우열을 정하지 않아요. 달라진 질문의 상위 원문을 읽고, 검색 품질과 실행 비용을 함께 근거로 모델 선택 이유를 적어 보세요.")
