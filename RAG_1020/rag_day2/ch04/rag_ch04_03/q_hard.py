# -*- coding: utf-8 -*-
# 4장 3강 퀴즈: 특정 근거를 놓치는 설정 찾기 (Hard: TODO를 직접 완성해요)
# 이 폴더에서 uv run q_hard.py로 실행해요.
# main.py를 먼저 실행해 chunks, vectors, model, exact_rows를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# k와 threshold를 바꿔 가며 한 조건씩 비교해요.
# 반환 개수뿐 아니라 한도 금액과 증빙 문장이 모두 남았는지 읽어 보세요.
q = "출장 숙박 비용 한도와 필요한 증빙은?"
results = {}
for k, threshold in [(1, None), (3, .88), (3, .90)]:
    # TODO: exact_rows에 k와 threshold를 넘겨 검색하세요.
    # TODO: results[(k, threshold)]에 (document_id, start) 목록을 담고 출력하세요.
    # TODO: 한도와 증빙 조건이 둘 다 남는지 원문으로 확인하세요.
    rows = exact_rows(q, chunks, vectors, model,
                      k=k, threshold=threshold)
    results[(k, threshold)] = [(r["document_id"], r["start"]) for r in rows]
    print(k, threshold, results[(k, threshold)])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert results[(1, None)] == [("travel", 0)]
assert results[(3, .88)] == [("travel", 0)], "0.88 이상은 travel:0 하나뿐이에요"
assert results[(3, .90)] == [], "0.90 이상인 후보가 없어 결과가 비어요"
travel0 = next(c for c in chunks if c["document_id"] == "travel" and c["start"] == 0)["text"]
assert "1박당 12만원" in travel0 and "영수증" in travel0
print("\n✅ 정답이에요!")
print("생각해 보기:", "golden.jsonl의 다른 개발 질문 하나로 k=1과 k=3을 비교하고, 추가된 청크가 어떤 질문 항목을 해결했는지 적어 보세요.")
