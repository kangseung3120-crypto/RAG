# -*- coding: utf-8 -*-
# 6장 1강 퀴즈: 검색 개수와 Context 예산을 따로 바꾸기 (Hard: TODO를 직접 완성해요)
# 이 폴더에서 uv run q_hard.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 question, pack_context를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 준비: main.py 끝에서 index를 닫았으므로 저장된 색인을 다시 열어요.
index = open_saved_index()

# 검색 후보 수와 Context 예산을 각각 바꿔요.
# 검색은 됐지만 Context에서 빠진 근거가 있는지 source_map과 packed를 함께 읽으세요.
results = {}
for k, budget in [(1, 300), (3, 200), (3, 300)]:
    # TODO: index.search로 k개를 검색하고 pack_context에 budget을 넣으세요.
    # TODO: results[(k, budget)]에 source_map의 document_id 목록을 담고 packed를 출력하세요.
    raise NotImplementedError


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert results[(1, 300)] == ["meal"], "k=1은 검색 단계에서 이미 meal:60 하나뿐이에요"
assert results[(3, 200)] == ["meal", "meal"], "k=3, 예산 200은 Context 단계에서 travel이 빠져요"
assert results[(3, 300)] == ["meal", "meal", "travel"]
index.close()
print("\n✅ 정답이에요!")
print("생각해 보기:", "같은 문서의 다른 청크까지 document_id로 중복 제거하면 어떤 근거가 빠지는지 설명해 보세요.")
