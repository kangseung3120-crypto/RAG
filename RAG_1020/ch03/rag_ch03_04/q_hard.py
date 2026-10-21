# -*- coding: utf-8 -*-
# 3장 4강 퀴즈: 문서별 분할 구간 모으기 (Hard: TODO를 직접 완성해요)
# 이 폴더에서 uv run q_hard.py로 실행해요.
# main.py를 먼저 실행해 chunks, documents를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 원문 ID별로 청크의 시작/끝 위치를 모으는 함수를 완성해요.
# 반환한 구간 목록으로 겹침과 빈 구간을 살펴보되 이 함수만으로 의미 보존이 판정되지는 않아요.
def coverage_by_document(chunks):
    result = {}
    for c in chunks:
        result.setdefault(c["document_id"], []).append((c["start"], c["end"]))
    return result


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
coverage = coverage_by_document(chunks)
for did, ranges in coverage.items():
    print(did, ranges)
assert coverage["travel"] == [(0, 80), (60, 140), (120, 148)]
assert len(coverage) == 12 and "travel-old" in coverage, "구버전 문서도 파일에 함께 있어요"
for d in documents:
    assert coverage[d["document_id"]][-1][1] == len(d["content"]), f"{d['document_id']}: 마지막 end가 원문 길이와 달라요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "원본 범위를 보관하는 작업과, 검색할 때 status: current만 고르는 필터가 왜 다른 단계인지 설명해 보세요.")
