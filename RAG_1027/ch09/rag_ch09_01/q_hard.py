# -*- coding: utf-8 -*-
# 9장 1강 퀴즈: 질문에 필요한 승인 조건 문장 고르기 (Hard: TODO를 직접 완성해요)
# 이 폴더에서 uv run q_hard.py로 실행해요.
# main.py를 먼저 실행해 selected를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 질문: "13만원 숙박을 예약하려고 해요. 어떻게 승인받아야 하나요?"
# 추출한 네 문장(selected) 중 승인 조건이 있는 문장만 원문 위치와 함께 골라요.
# TODO: selected에서 승인 조건이 들어 있는 문장만 chosen에 담으세요. (start, end, text) 형태를 유지해요.
# TODO: chosen을 한 줄씩 출력하세요.
chosen = [(start, end, text) for start, end, text in selected
          if "승인" in text]
for row in chosen:
    print(row)

# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert [(s, e) for s, e, _ in chosen] == [(53, 92), (92, 123)], "승인 문장은 53~92, 92~123 두 개예요"
assert any(all(w in t for w in ["예약 전에", "담당 임원", "서면"]) for _, _, t in chosen), "예약 전 · 담당 임원 · 서면을 빠뜨리지 않아요"
print("원문 위치로 다시 읽기:", parent["content"][53:92])
print("\n✅ 정답이에요!")
print("생각해 보기:", "한도를 설명하려고 첫 문장(0~28)도 함께 넣는다면 문자 예산이 얼마 이상이어야 하는지 계산해 보세요.")
