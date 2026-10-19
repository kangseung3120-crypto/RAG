# -*- coding: utf-8 -*-
# 1장 4강 퀴즈: 상황에 맞는 비교 후보 고르기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 (main.py의 변수는 쓰지 않아요)를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

def choose_input(document_tokens, available, repeated, cache_supported):
    # 우선 문서가 예산 안에 들어가는지 확인해요. 길이가 넘으면 반복 요청 여부와 무관하게 입력 범위를 줄여야 해요.
    if document_tokens > available:
        return "RAG 또는 문서 범위 축소"
    # 입력이 들어갈 때만 반복 여부와 캐시 지원을 고려해요.
    # 실제 속도나 비용 절감은 선택한 모델과 서비스에서 따로 측정해야 해요.
    if repeated and cache_supported:
        return "전체 입력 + prefix cache 비교"
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
