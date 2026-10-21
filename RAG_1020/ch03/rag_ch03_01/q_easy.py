# -*- coding: utf-8 -*-
# 3장 1강 퀴즈: 입력값을 확인하고 경계 바꾸기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 text, windows를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 이동 간격이 0 이하가 되지 않게 입력을 먼저 검사하는 과제예요.
# 빈칸(____)을 채우세요. 허용 범위는 0 <= overlap < size예요.
def checked_windows(text, size, overlap):
    if not 0 <= overlap < size:
        raise ValueError("0 <= overlap < size")
    return windows(text, size, overlap)


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
pieces = checked_windows(text, 100, 20)
for start, end, piece in pieces:
    print(f"[{start}:{end}]", piece)
assert [(s, e) for s, e, _ in pieces] == [(0, 100), (80, 148)]
assert "한도 초과 숙박은 예약 전에 담당 임원의 서면 승인을 받아야 합니다" in pieces[0][2], "100/20이면 승인 문장이 첫 청크에 들어가요"
for size, overlap in [(80, 80), (80, -1)]:
    try:
        checked_windows(text, size, overlap)
        raise AssertionError(f"{size}/{overlap}은 ValueError가 나야 해요")
    except ValueError as error:
        print(f"{size}/{overlap} → ValueError:", error)
print("\n✅ 정답이에요!")
print("생각해 보기:", "overlap을 0→10→20으로 바꾸며 저장 문자 수와 승인 문장이 들어간 청크를 비교해 보세요.")
