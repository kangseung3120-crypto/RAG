"""9-2: 실제 BM25 재검색과 종료. --generate는 Ollama 연결."""
import argparse
import json
from pathlib import Path
from rag_core import bm25, build_context, generate_ollama

parser = argparse.ArgumentParser()
parser.add_argument("--generate", action="store_true")
args = parser.parse_args()
chunks = json.loads(Path("chunks.json").read_text(encoding="utf-8"))
current = [c for c in chunks if c["metadata"]["status"] == "current"]
golden = [json.loads(s) for s in Path("golden.jsonl").read_text(encoding="utf-8").splitlines()]
question = next(g["question"] for g in golden if g["question_id"] == "q10")

# 기본 실습은 사람이 준비한 질의를 순서대로 실행하는 제한된 검색 루프예요.
# LLM이 자율적으로 재작성하거나 근거 충분성을 판정하는 코드는 agent.py에서 다뤄요.
def search_loop(queries, topic, max_searches=2):
    trace, seen = [], set()
    for query in queries[:max_searches]:
        if query in seen:
            return [], trace, "repeated_query"
        seen.add(query)
        # 제목에 주제어가 있는지로 관련 후보를 거르는 간단한 규칙이에요.
        # 제목이 맞아도 본문에 필요한 서류나 예외가 없을 수 있어 candidates_ready가 정답 보장은 아니에요.
        candidates = bm25(query, current, k=3)
        on_topic = [c for c in candidates if topic in c["metadata"]["title"]]
        # trace에는 각 검색이 어떤 후보를 찾았는지 남겨요.
        # 종료 사유를 반환해 반복 질의, 횟수 한도, 후보 확보를 구분할 수 있게 해요.
        trace.append({"query": query, "hits": [(c["document_id"], c["start"]) for c in candidates],
                      "on_topic": len(on_topic)})
        if on_topic:
            return on_topic, trace, "candidates_ready"
    return [], trace, "search_limit"

# 원질문과 수정한 검색문을 비교하고, 같은 질의 반복과 횟수 제한도 따로 실행해 봐요.
queries = [question, "교육비 지원 수강 완료 후 제출합니다"]
rows, trace, status = search_loop(queries, "교육비")
print("STEP1", json.dumps(trace, ensure_ascii=False), status)
print("STEP2", rows[0]["text"] if rows else "없음")
print("STEP3", search_loop([question, question], "교육비")[2])
print("STEP4", search_loop(queries, "교육비", max_searches=1)[2])
# 후보를 찾은 뒤에도 실제 답변은 원질문과 Context를 사용해 생성해요.
# --generate가 없으면 검색과 종료 조건까지만 확인해요.
if args.generate:
    context, sources = build_context(rows)
    print(generate_ollama(question, context, sources))
else:
    print("GENERATION_NOT_RUN: 실제 재검색 완료; title 검사는 근거 충실성 평가가 아닙니다.")
