# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# 실제 후보 중 식비 청크 두 개가 먼저 나오도록 순서를 구성한 계산 연습이에요.
# 상위 두 청크가 모두 같은 문서라면 정답 문서 두 개 중 한 개만 찾은 셈이에요.
item = next(g for g in dev if g["question_id"] == "q06")
ranked = bm25(item["question"], current, k=5)
expected = set(item["relevant_document_ids"])
lookup = {(r["document_id"], r["start"]): r for r in ranked}
ordered = [lookup[("meal", 60)], lookup[("meal", 0)], lookup[("travel", 0)]]
found = {r["document_id"] for r in ordered[:2]}
recall = len(found & expected) / len(expected)
print(sorted(found), recall)
