# -*- coding: utf-8 -*-
# 1장 4강 퀴즈: 상황에 맞는 비교 후보 고르기 (Hard: 교안의 TODO를 직접 완성해요)
# 이 폴더에서 uv run q_hard.py로 실행해요.
# main.py를 먼저 실행해 (main.py의 변수는 쓰지 않아요)를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from RAG_1019.ch01.rag_ch01_04.main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 입력 길이, 반복 여부, 캐시 지원 여부로 먼저 비교할 방식을 고르는 과제예요.
# 성능이나 비용을 실측한 결론이 아니라 실험 후보를 정하는 간단한 규칙이에요.
def choose_input(document_tokens, available, repeated, cache_supported):
    # TODO 1: 자료가 문서 예산을 넘는 경우를 처리하세요.
    if document_tokens > available:
        return "RAG 또는 문서 범위 축소"
    # TODO 2: 반복 요청이며 캐시를 지원하는 경우를 처리하세요.
    if repeated and cache_supported:
        return "전체 입력 + prefix cache 비교"
    # TODO 3: 나머지 경우의 비교 후보를 반환하세요.
    return "전체 입력부터 비교"


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
cases = [((3000, 6000, True, True), "전체 입력 + prefix cache 비교"),
         ((900000, 6000, True, True), "RAG 또는 문서 범위 축소"),
         ((3000, 6000, False, False), "전체 입력부터 비교"),
         ((3000, 6000, True, False), "전체 입력부터 비교")]
for case, expected in cases:
    print(case, "->", choose_input(*case))
    assert choose_input(*case) == expected, (case, expected)
print("\n✅ 정답이에요!")
print("생각해 보기:", "캐시를 지원해도 예산 초과 조건을 가장 먼저 확인하는 이유를 설명해 보세요.")
