# -*- coding: utf-8 -*-
# 1장 1강 퀴즈: 현행 규정 검색 함수 만들기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 documents, current를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

def find_policy(term, current_only=True):
    # 공백만 입력한 경우를 먼저 막아요. 빈 문자열은 모든 본문에 포함되므로 그대로 검색하면 전체 문서가 나와요.
    if not term.strip():
        raise ValueError("검색어를 입력하세요.")
    # current_only=True면 현재 규정만, False면 과거 규정까지 검색해요.
    # 같은 검색어로 두 범위의 결과를 비교해 필터의 역할을 확인해요.
    candidates = current if current_only else documents
    return [d for d in candidates if term in d["content"]]


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
ids = lambda docs: [d["document_id"] for d in docs]
print("숙박 비용 (현행만):", ids(find_policy("숙박 비용")))
print("숙박 비용 (구버전 포함):", ids(find_policy("숙박 비용", False)))
print("호텔비:", ids(find_policy("호텔비")))
print("개인 취미:", ids(find_policy("개인 취미")))
try:
    find_policy("   ")
    raise AssertionError("공백 검색어는 ValueError가 나야 해요.")
except ValueError as error:
    print("공백 검색어:", error)

assert ids(find_policy("숙박 비용")) == ["travel"]
assert ids(find_policy("숙박 비용", False)) == ["travel", "travel-old"]
assert ids(find_policy("호텔비")) == []
assert ids(find_policy("개인 취미")) == ["education"]
print("\n✅ 정답이에요!")
print("생각해 보기:", "호텔비가 빈 목록인 이유(검색 표현 문제)와, 개인 취미는 education이 검색돼도 답할 수 없는 이유(근거 부족)를 구분해 설명해 보세요.")
