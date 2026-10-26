# -*- coding: utf-8 -*-
# 7장 2강 퀴즈: RRF 결과에서 원문마다 한 청크씩 고르기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 rankings, reciprocal_rank_fusion를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 서로 다른 원문에서 한 청크씩 골라 문서 다양성을 확보해요.
fused = reciprocal_rank_fusion(rankings, k=6)
selected, seen_documents = [], set()
for row in fused:
    did = row["document_id"]
    if did not in seen_documents:
        selected.append(row)
        seen_documents.add(did)
    if len(selected) == 2: break
print("문서 다양성 실습:", [(r["document_id"], r["start"]) for r in selected])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
picked = [(r["document_id"], r["start"]) for r in selected]
plain = [(r["document_id"], r["start"]) for r in fused[:2]]
print("그냥 상위 2개:", plain)
assert picked == [("meal", 60), ("travel", 0)], "원문마다 하나씩이면 meal 60, travel 0이에요"
assert plain == [("meal", 60), ("meal", 0)]
assert seen_documents == {"meal", "travel"}
print("빠진 청크 meal 0:", next(r["text"] for r in fused if r["document_id"] == "meal" and r["start"] == 0)[:40])
print("\n✅ 정답이에요!")
print("생각해 보기:", "원문마다 한 청크만 고르면 식비 금액(meal 0)이 빠져요. q06의 세 항목(식비 · 숙박비 · 합산 여부)을 모두 담으려면 몇 개를 어떻게 골라야 할지 적어 보세요.")
