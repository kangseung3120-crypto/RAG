# -*- coding: utf-8 -*-
# 7장 4강 퀴즈: 같은 검색 문장을 검색 전에 한 번만 남기기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 question, variants, current, bm25를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 같은 검색 표현이 두 번 들어간 목록이에요. 검색 전에 중복을 없애 같은 BM25 계산을 반복하지 않아요.
# 순서는 처음 나온 순서를 유지하세요.
queries = [question, variants[1], variants[1], variants[2]]
unique_queries = list(dict.fromkeys(queries))
all_rows = []
for query in unique_queries: all_rows.extend(bm25(query, current, k=3))
print("검색 횟수:", len(unique_queries))
print("반환 청크 수:", len(all_rows))


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert unique_queries == [question, variants[1], variants[2]], "순서를 유지한 채 중복만 빠져야 해요"
assert len(all_rows) == 5, "질의 3개의 결과는 0 + 3 + 2 = 5개예요"
unique_chunks = list(dict.fromkeys(r["chunk_id"] for r in all_rows))
print("chunk_id 중복 제거 후:", len(unique_chunks))
assert len(unique_chunks) == 3, "청크 중복은 검색 뒤에 chunk_id로 따로 제거해요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "set(queries)로 중복을 제거하면 결과가 어떻게 달라질 수 있는지, 원질문을 항상 첫 번째로 두는 이유와 함께 설명해 보세요.")
