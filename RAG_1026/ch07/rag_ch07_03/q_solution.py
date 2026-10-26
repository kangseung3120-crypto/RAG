# -*- coding: utf-8 -*-
# 7장 3강 퀴즈: 정답 후보를 빼고 다시 재정렬하기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 run, candidates, model를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 출장 후보를 제거하고 남은 후보만 다시 점수화해요.
reduced = [row for row in candidates if row["document_id"] != "travel"]
new_pairs = [(run["question"], row["text"]) for row in reduced]
new_values = model.predict(new_pairs, batch_size=4, show_progress_bar=False)
print("후보 제거 실습:", [row["document_id"] for row in reduced], len(new_values))


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert [r["document_id"] for r in reduced] == ["meal", "meal", "meeting", "vpn", "leave"]
assert len(new_values) == 5
best = reduced[max(range(len(new_values)), key=lambda i: float(new_values[i]))]
print("새 1위:", best["document_id"], best["start"])
assert all("12만원" not in r["text"] for r in reduced), "숙박비 금액(1박당 12만원)은 이제 어느 후보에도 없어요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "재정렬 전 후보 수를 줄여 travel 0이 후보에서 빠진 경우를 떠올리고, 검색 단계와 재정렬 단계 중 어디를 고쳐야 할지 적어 보세요.")
