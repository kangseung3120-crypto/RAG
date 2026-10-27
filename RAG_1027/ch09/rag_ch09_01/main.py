"""9-1: 공통 청크를 실제 원문으로 확장하고 문장 단위로 압축."""
import argparse
import json
import re
from pathlib import Path
from rag_core import bm25, build_context, generate_ollama

parser = argparse.ArgumentParser()
parser.add_argument("--generate", action="store_true")
args = parser.parse_args()
# 검색은 작은 Child 청크에서 수행하고 document_id로 더 큰 Parent 원문을 찾아요.
# 현재 규정만 대상으로 맞춰 과거 버전의 부모 본문을 섞지 않아요.
docs = json.loads(Path("documents.json").read_text(encoding="utf-8"))
chunks = json.loads(Path("chunks.json").read_text(encoding="utf-8"))
current = [c for c in chunks if c["metadata"]["status"] == "current"]
parents = {d["document_id"]: d for d in docs if d["metadata"]["status"] == "current"}
question = "출장 숙박 비용 한도는?"
hits = bm25(question, current, k=3)
child = next(c for c in hits if c["document_id"] == "travel")
parent = parents[child["document_id"]]
print("STEP1", "child", child["start"], child["end"], len(child["text"]))
print(child["text"])
print("parent", len(parent["content"]), parent["content"])
# 같은 문서의 Child가 여러 개 검색돼도 Parent 본문은 한 번만 넣어요.
# retrieved_child_ids는 어떤 작은 근거 때문에 부모를 확장했는지 추적하는 기록이에요.
seen = set()
expanded = []
for c in hits:
    if c["document_id"] not in seen:
        p = parents[c["document_id"]]
        expanded.append({**c, "chunk_id": f"{p['document_id']}:parent:{p['metadata']['version']}",
                         "retrieved_child_ids": [h["chunk_id"] for h in hits
                                                 if h["document_id"] == p["document_id"]],
                         "text": p["content"], "start": 0, "end": len(p["content"])})
        seen.add(c["document_id"])
print("STEP2", "검색청크", len(hits), "부모본문", len(expanded))
# 마침표로 끝나는 문장과 원문 위치를 추출한 뒤 조건 단어가 있는 문장만 남겨요.
# 이 단순 규칙은 마침표가 없는 마지막 문장이나 복잡한 약어를 처리하는 일반 문장 분리기가 아니에요.
spans = [(m.start(), m.end(), m.group().strip())
         for m in re.finditer(r"[^.]+\.", parent["content"])]
terms = ["한도", "초과", "승인", "영수증"]
selected = [s for s in spans if any(t in s[2] for t in terms)]
print("STEP3", [(start, end, text) for start, end, text in selected])
# 문장 단위로 예산에 들어가는 근거를 골라 압축 효과를 확인해요.
# 짧아진 길이만 보지 말고 한도 초과와 사전 승인 같은 예외 조건이 사라졌는지도 살펴보세요.
for budget in [70, 140]:
    kept, used = [], 0
    for start, end, text in selected:
        if used + len(text) + 1 <= budget:
            kept.append(text)
            used += len(text) + 1
    print("budget", budget, "남은문장", len(kept), "chars", used, " ".join(kept))
# --generate를 지정했을 때만 부모 전체를 근거로 실제 답변을 생성해요.
# 기본 실행의 추출 문장 출력은 LLM이 작성한 요약이 아니에요.
if args.generate:
    context, sources = build_context(expanded)
    print(generate_ollama("13만원짜리 숙박도 정산할 수 있나요?", context, sources))
else:
    print("GENERATION_NOT_RUN: 부모 확장과 문장 추출은 실행, 답변 생성은 선택 실습")
