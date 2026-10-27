# -*- coding: utf-8 -*-
# 8장 4강 퀴즈: comparison_08.json에서 q10의 실패 위치 기록하기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 comparison_08.json를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 저장된 비교 파일은 split → 검색 방법 → rows 순서로 중첩돼 있어요.
# 검색 모델을 다시 실행하지 않고 파일만 읽어 dev의 Hybrid 결과에서 q10을 찾아요.
saved = json.loads(Path("comparison_08.json").read_text(encoding="utf-8"))
hybrid_rows = saved["dev"]["hybrid"]["rows"]
q10 = next(r for r in hybrid_rows if r["question_id"] == "q10")
print(q10["retrieved_document_ids"], q10["recall"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
bm25_q10 = next(r for r in saved["dev"]["bm25"]["rows"] if r["question_id"] == "q10")
print("BM25 q10:", bm25_q10["retrieved_document_ids"], bm25_q10["recall"])
assert q10["retrieved_document_ids"] == ["education", "meal", "travel"] and q10["recall"] == 1.0
assert bm25_q10["retrieved_document_ids"] == [] and bm25_q10["recall"] == 0.0
print("문서 Recall 1.0이지만 증빙(수료증과 영수증)은 education@60 청크에 있는지 따로 확인해요")
print("\n✅ 정답이에요!")
print("생각해 보기:", "Hybrid의 q10 Top-3 청크 본문에 수료증과 영수증이 실제로 있는지 확인하고, 없다면 다음에 시험할 변경(Parent 확장 · 질의 변형 · 재정렬) 하나를 이유와 함께 골라 보세요.")
