# -*- coding: utf-8 -*-
# 9장 4강 퀴즈: 숙박 한도 행을 고르고 출처까지 출력하기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 rows를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 계산에 사용한 금액과 원문 ID, URL을 함께 출력해 숫자의 출처를 확인해요.
chosen = next(r for r in rows if r["document_id"] == "travel")
answer_value = chosen["limit_won"]
print(answer_value, chosen["document_id"], chosen["source_url"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert answer_value == 120000 and chosen["document_id"] == "travel"
assert chosen["source_url"].endswith("/travel")
assert "1박당" in by_id["travel"]["content"] and "숙박 영수증" in by_id["travel"]["content"]
print("최종 답에는 단위(1박당)와 증빙(숙박 영수증)도 함께 적어요")
print("\n✅ 정답이에요!")
print("생각해 보기:", "visual_pages/travel.png를 열어 12만원, 1박당, 숙박 영수증, 한도 초과 승인 문장이 잘리지 않고 보이는지 확인해 보세요.")
