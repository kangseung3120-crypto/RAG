# -*- coding: utf-8 -*-
# 5장 4강 퀴즈: 잘못된 삭제 대상 고치기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 old_ids, new_ids, stale_ids를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 옛 ID에는 있지만 새 ID에는 없는 집합을 계산하는 과제예요.
# 삭제 대상과 새 ID의 교집합이 비어 있어야 새로 만든 청크를 지우지 않아요.
to_remove = old_ids - new_ids
print("삭제 대상 수:", len(to_remove))
print("새 ID를 삭제하는가:", bool(to_remove & new_ids))


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert isinstance(to_remove, set) and len(to_remove) == 3, "삭제 대상은 옛 travel 청크 3개예요"
assert not (to_remove & new_ids), "새 ID가 삭제 대상에 섞이면 새 청크까지 지워져요"
assert to_remove == stale_ids
print("합집합으로 잘못 지정하면:", len(old_ids | new_ids), "개 삭제 → 새 청크도 사라져요")
print("\n✅ 정답이에요!")
print("생각해 보기:", "ANN 모형에서 visited를 [0, 1, 2, 4]로 바꾸면 선택 결과와 겹침 비율이 어떻게 될지 먼저 예상한 뒤 실행해 보세요.")
