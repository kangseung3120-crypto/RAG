# -*- coding: utf-8 -*-
# 9장 2강 퀴즈: 같은 질의 반복과 다른 표현 재검색 비교하기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 question, search_loop를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 같은 질문을 두 번 넣은 경우와 표현을 바꾼 경우를 같은 검색 한도에서 비교해요.
# 상태, 검색 기록 수, 반환된 청크 위치를 함께 읽어요.
same = [question, question]
changed = [question, "교육비 지원 수강 완료 후 제출합니다"]
results = {}
for name, items in [("same", same), ("changed", changed)]:
    rows, trace, status = search_loop(items, "교육비", max_searches=2)
    results[name] = (status, len(trace), [c["start"] for c in rows])
    print(name, results[name])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert results["same"] == ("repeated_query", 1, []), "같은 질의는 두 번째에서 멈춰요"
assert results["changed"] == ("candidates_ready", 2, [60, 0]), "다른 표현은 두 번째 검색에서 education 60, 0을 찾아요"
print("education@0만 읽으면 증빙이 없어요 → 제목 검사 통과 ≠ 근거 충분")
print("\n✅ 정답이에요!")
print("생각해 보기:", "max_searches=1로 바꾸면 changed의 상태가 어떻게 되는지 먼저 예상하고, 실행해서 확인해 보세요.")
