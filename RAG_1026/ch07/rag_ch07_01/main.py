"""7-1: 공통 청크의 토큰, BM25, 실제 E5 검색 비교."""
import json
import math
from collections import Counter
from pathlib import Path
from rag_core import tokenize, bm25, DenseIndex

# 같은 청크와 질문으로 BM25와 E5를 비교해요.
# 검색 대상은 현재 규정으로 맞추고, golden은 질문과 비교 기준을 제공해요.
chunks = json.loads(Path("chunks.json").read_text(encoding="utf-8"))
current = [c for c in chunks if c["metadata"]["status"] == "current"]
golden = [json.loads(s) for s in Path("golden.jsonl").read_text(encoding="utf-8").splitlines()]
print("STEP1", len(chunks), len(current))
# 공백/기호 기준 토크나이저에서는 영수증, 영수증을, 영수증으로가 다른 토큰이에요.
# 이 차이가 키워드 검색 실패로 이어지는지 뒤 결과와 연결해 보세요.
travel = next(c for c in current if c["document_id"] == "travel" and c["start"] == 0)
print("질문 토큰:", tokenize(golden[4]["question"]))
print("본문 토큰:", tokenize(travel["text"])[:10])
print("서로 다른 토큰:", tokenize("영수증 영수증을 영수증으로"))

# N은 청크 수, df는 숙박 토큰이 한 번이라도 등장한 청크 수예요.
# 드문 단어에 더 높은 값을 주는 IDF가 BM25 점수에 어떻게 들어가는지 확인해요.
bags = [Counter(tokenize(c["text"])) for c in current]
df = sum("숙박" in bag for bag in bags)
N = len(bags)
idf = math.log(1 + (N - df + .5) / (df + .5))
print("STEP2", "N", N, "df(숙박)", df, "IDF", round(idf, 4))
for q in ["출장 숙박", "영수증", "영수증을", "영수증으로"]:
    hits = bm25(q, current, k=3)
    print(q, [(r["document_id"], r["start"], round(r["score"], 4)) for r in hits])

# DenseIndex는 실제 E5 벡터와 메모리 Qdrant를 준비해요.
# 여러 질문에 같은 색인을 재사용해 질문마다 문서를 다시 임베딩하지 않아요.
dense = DenseIndex(chunks)
runs = []
try:
    # 각 질문에서 두 검색기의 상위 6개를 저장해 나중에 RRF와 재정렬 입력으로 사용해요.
    # 두 점수는 척도가 다르므로 숫자 크기 자체보다 문서 순위와 본문을 비교해요.
    for item in golden[:12]:
        q = item["question"]
        sparse = bm25(q, current, k=6)
        semantic = dense.search(q, k=6)
        runs.append({"question_id": item["question_id"], "question": q,
                     "bm25": sparse, "dense": semantic})
        if item["question_id"] in {"q05", "q06", "q10", "q11"}:
            print("STEP3", item["question_id"], q)
            for name, rows in [("BM25", sparse), ("Dense", semantic)]:
                print(name, [(r["document_id"], r["start"], round(r["score"], 4))
                             for r in rows[:3]])
# 실패하더라도 Qdrant 연결은 닫아요. 모든 질문 처리가 끝나면 실제 검색 결과를 JSON으로 저장해요.
finally:
    dense.close()
Path("search_runs_07.json").write_text(json.dumps(runs, ensure_ascii=False, indent=2), encoding="utf-8")
