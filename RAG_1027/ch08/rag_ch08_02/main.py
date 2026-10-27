"""8-2: 같은 golden과 실제 BM25 검색 결과로 Hit/Recall 계산."""
import json
from pathlib import Path
from rag_core import bm25

# 동일한 현재 청크와 dev 질문으로 k만 바꿔 비교해요.
# 평가 단위는 청크가 아니라 원문 ID이므로 중복 청크를 set으로 합쳐 계산해요.
chunks = json.loads(Path("chunks.json").read_text(encoding="utf-8"))
current = [c for c in chunks if c["metadata"]["status"] == "current"]
golden = [json.loads(s) for s in Path("golden.jsonl").read_text(encoding="utf-8").splitlines()]
dev = [g for g in golden if g["split"] == "dev"]
print("STEP1")
item = next(g for g in dev if g["question_id"] == "q06")
ranked = bm25(item["question"], current, k=5)
# Hit은 정답 문서를 하나라도 찾으면 1이고 Recall은 찾은 정답 문서 수 / 전체 정답 문서 수예요.
# 정답 문서가 두 개이면 한 개만 찾아도 Hit=1이지만 Recall=0.5예요.
for k in [1, 3, 5]:
    found = {r["document_id"] for r in ranked[:k]}
    expected = set(item["relevant_document_ids"])
    print(k, sorted(found), int(bool(found & expected)), len(found & expected)/len(expected))

print("STEP2")
# 먼저 질문별 값을 계산한 뒤 질문 수로 나눠 평균을 내요.
# 정답 문서가 없는 질문은 Recall 분모가 0이므로 이 검색 평균에서 제외해요.
for k in [1, 3, 5]:
    rows = []
    for g in dev:
        hits = bm25(g["question"], current, k=5)[:k]
        found = {r["document_id"] for r in hits}
        expected = set(g["relevant_document_ids"])
        if expected:
            rows.append((g["question_id"], int(bool(found & expected)), len(found & expected)/len(expected)))
    print("k", k, "분모", len(rows),
          "Hit", round(sum(r[1] for r in rows)/len(rows), 4),
          "Recall", round(sum(r[2] for r in rows)/len(rows), 4))
    # 평균만 보면 일부 질문의 실패를 놓칠 수 있어 질문별 결과도 출력해요.
    # 제외된 답없음 질문은 보류 성능을 평가할 때 따로 사용해야 해요.
    if k == 3:
        print("질문별", rows)
print("STEP3", "검색평가 제외", [g["question_id"] for g in dev if not g["answerable"]])