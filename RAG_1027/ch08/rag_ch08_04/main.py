"""8-4: 실제 검색의 개선 전후. dev로 비교하고 test는 별도로 집계합니다."""
import json
from pathlib import Path
from rag_core import bm25, DenseIndex, evaluate, retrieve

# 자료와 k=3을 고정하고 BM25, Dense, Hybrid만 바꿔 비교해요.
# 설정 선택은 dev로 하고 test 결과를 보고 반복 조정하지 않아야 최종 평가 의미가 유지돼요.
chunks = json.loads(Path("chunks.json").read_text(encoding="utf-8"))
golden = [json.loads(s) for s in Path("golden.jsonl").read_text(encoding="utf-8").splitlines()]
dense = DenseIndex(chunks)
reports = {}
try:
    for split in ["dev", "test"]:
        selected = [g for g in golden if g["split"] == split]
        by_method = {}
        for method in ["bm25", "dense", "hybrid"]:
            # lambda의 m=method는 이번 반복의 검색 방식을 기본값으로 고정해요.
            # 같은 평가 함수에 검색기만 갈아 끼워 질문과 채점 기준 차이를 줄여요.
            search = lambda q, cat=None, m=method: retrieve(q, chunks, m, dense, k=3, category=cat)
            by_method[method] = evaluate(selected, search)
            r = by_method[method]
            print("STEP1", split, method, r["answerable_count"], round(r["hit_at_k"], 4), round(r["recall_at_k"], 4))
        # 평균 외에 같은 question_id끼리 Recall을 비교해 개선된 질문과 악화된 질문을 나눠요.
        # 전체 평균이 좋아져도 특정 질문에서 필요한 근거를 잃을 수 있어요.
        a = {r["question_id"]: r for r in by_method["bm25"]["rows"] if r["answerable"]}
        b = {r["question_id"]: r for r in by_method["hybrid"]["rows"] if r["answerable"]}
        wins = [qid for qid in a if b[qid]["recall"] > a[qid]["recall"]]
        losses = [qid for qid in a if b[qid]["recall"] < a[qid]["recall"]]
        print("STEP2", split, "wins", wins, "losses", losses)
        # 변화가 있는 질문의 검색 문서 ID를 출력해 개선/악화 원인을 원문으로 돌아가 확인해요.
        for qid in wins + losses:
            print(qid, a[qid]["retrieved_document_ids"], "->", b[qid]["retrieved_document_ids"])
        reports[split] = by_method
finally:
    dense.close()
Path("comparison_08.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
