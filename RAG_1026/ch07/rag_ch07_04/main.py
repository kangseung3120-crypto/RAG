"""7-4: 같은 질문의 수동 재작성, 실제 검색, 합집합."""
import json
from pathlib import Path
from rag_core import bm25

# 원질문과 사람이 작성한 검색 표현 두 개를 같은 BM25 검색기에 넣어요.
# 기본 실습의 재작성 문장은 생성 모델 출력이 아니에요.
chunks = json.loads(Path("chunks.json").read_text(encoding="utf-8"))
current = [c for c in chunks if c["metadata"]["status"] == "current"]
golden = [json.loads(s) for s in Path("golden.jsonl").read_text(encoding="utf-8").splitlines()]
question = next(g["question"] for g in golden if g["question_id"] == "q10")
variants = [question, "교육비 지원 수강 완료 후 제출합니다", "직무 교육비 정산 제출합니다"]
print("STEP1", question)
for q in variants:
    rows = bm25(q, current, k=3)
    print(q, [(r["document_id"], r["start"]) for r in rows])
# 서로 다른 질의에서 찾은 결과를 chunk_id로 합쳐 중복을 제거해요.
# 이 합집합은 첫 등장 순서이며 통합 관련도 순위를 다시 계산한 결과는 아니에요.
union = {}
for q in variants:
    for row in bm25(q, current, k=3):
        union.setdefault(row["chunk_id"], row)
print("STEP2", "합집합", len(union), [(r["document_id"], r["start"]) for r in union.values()])
# 교육비 근거 본문을 읽어 실제 필요한 서류가 포함됐는지 확인해요.
# 결과 수가 늘어난 것과 질문에 필요한 근거를 찾은 것은 구분해야 해요.
for row in union.values():
    if row["document_id"] == "education":
        print("교육비 근거:", row["text"])
print("STEP3", "중복 질의 제거", len(list(dict.fromkeys(variants + [variants[0]]))))
