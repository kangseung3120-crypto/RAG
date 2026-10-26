"""7-2: 7-1에서 실제 검색한 두 순위 목록을 RRF로 결합."""
import json
from collections import defaultdict
from pathlib import Path
from rag_core import reciprocal_rank_fusion

# 이 강의 prepare.py로 만든 두 검색 순위 목록을 읽어요.
# 같은 q06의 결과를 써야 RRF가 서로 다른 질문의 후보를 섞지 않아요.
runs = json.loads(Path("search_runs_07.json").read_text(encoding="utf-8"))
run = next(r for r in runs if r["question_id"] == "q06")
rankings = [run["bm25"], run["dense"]]
print("STEP1")
for name, rows in zip(["BM25", "Dense"], rankings):
    print(name, [(r["document_id"], r["start"]) for r in rows])

# scores는 청크별 합산값, contributions는 검색기마다 더한 값, lookup은 원래 청크 정보예요.
# 최종 점수뿐 아니라 어떤 순위에서 점수를 얻었는지 설명할 수 있도록 나눠 저장해요.
scores = defaultdict(float)
contributions = defaultdict(list)
lookup = {}
# 순위는 1부터 시작하고 각 검색기에서 1 / (60 + 순위)를 더해요.
# 두 검색기에서 모두 나온 청크는 두 값을 받으며 원래 BM25/코사인 점수를 직접 더하지 않아요.
for name, rows in zip(["BM25", "Dense"], rankings):
    for rank, row in enumerate(rows, 1):
        cid = row["chunk_id"]
        lookup[cid] = row
        value = 1 / (60 + rank)
        scores[cid] += value
        contributions[cid].append((name, rank, round(value, 6)))
# 합산값이 높은 순으로 정렬하고 동점은 청크 ID로 고정해요.
# contributions를 읽으면 특정 후보가 순위에서 올라온 이유를 확인할 수 있어요.
order = sorted(scores, key=lambda cid: (-scores[cid], cid))
print("STEP2")
for cid in order[:5]:
    row = lookup[cid]
    print(row["document_id"], row["start"], contributions[cid], round(scores[cid], 6))
print("STEP3", "합집합", len(order))
# 각 검색기의 후보 수를 바꾸되 최종 반환 개수는 3으로 고정해요.
# 후보를 일찍 잘라 버리면 RRF가 필요한 청크를 되살릴 수 없어요.
for candidate_k in [2, 4, 6]:
    result = reciprocal_rank_fusion([rows[:candidate_k] for rows in rankings], k=3)
    print("각 검색기 후보", candidate_k, "최종", [(r["document_id"], r["start"]) for r in result])
