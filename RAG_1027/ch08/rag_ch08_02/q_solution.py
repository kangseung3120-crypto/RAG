# -*- coding: utf-8 -*-
# 8장 2강 퀴즈: 같은 문서 청크가 앞에 오면 Recall@2는? (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 current, dev, bm25를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 상위 두 청크가 모두 같은 문서라면 정답 문서 두 개 중 한 개만 찾은 셈이에요.
item = next(g for g in dev if g["question_id"] == "q06")
ranked = bm25(item["question"], current, k=5)
expected = set(item["relevant_document_ids"])
lookup = {(r["document_id"], r["start"]): r for r in ranked}
ordered = [lookup[("meal", 60)], lookup[("meal", 0)], lookup[("travel", 0)]]
found = {r["document_id"] for r in ordered[:2]}
recall = len(found & expected) / len(expected)
print(found, recall)


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert found == {"meal"} and recall == 0.5, "청크 2개가 모두 meal이라 Recall@2는 0.5예요"
documents_first = set(list(dict.fromkeys(r["document_id"] for r in ordered))[:2])
print("문서를 먼저 중복 제거하면:", sorted(documents_first), len(documents_first & expected) / len(expected))
assert documents_first == {"meal", "travel"}
print("\n✅ 정답이에요!")
print("생각해 보기:", "q10의 BM25 결과가 빈 목록인 이유가 문서가 없어서인지 검색 실패인지, education 원문을 읽고 설명해 보세요.")
