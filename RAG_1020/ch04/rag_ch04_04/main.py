"""4장 4강: 실제 small 기준선. --compare-base는 추가 모델 다운로드가 필요합니다."""
import argparse
import json
import time
from pathlib import Path
from rag_core import evaluate
from embedding_io import load_chunks, load_vectors, load_model, exact_rows, MODEL_ID

# 기본 실행은 small만 평가하고 --compare-base를 주면 base를 추가로 내려받아 비교해요.
parser = argparse.ArgumentParser()
parser.add_argument("--compare-base", action="store_true")
args = parser.parse_args()
# 모델 선택에는 dev 질문만 사용해요. 최종 확인용 test 질문으로 설정을 고르면 평가가 낙관적으로 치우쳐요.
chunks = load_chunks()
golden = [json.loads(s) for s in Path("golden.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
dev = [g for g in golden if g["split"] == "dev"]
models_to_run = [MODEL_ID] + (["intfloat/multilingual-e5-base"] if args.compare_base else [])
results = {}

# %% 1. 모델만 바꿔 동일한 개발 질문 평가
# 모델이 바뀌면 문서와 질문을 모두 같은 새 모델로 임베딩해야 해요.
# small의 저장 벡터와 base의 질문 벡터를 섞으면 차원과 의미 공간이 맞지 않아요.
for model_id in models_to_run:
    model = load_model(model_id)
    vectors = load_vectors(chunks) if model_id == MODEL_ID else model.encode(
        ["passage: " + c["text"] for c in chunks], normalize_embeddings=True)
    # 자료와 k=3을 고정하고 검색 함수에 모델만 다르게 연결해요.
    # query_seconds는 질문 임베딩과 검색 평가 시간이며 모델 다운로드/문서 색인 시간은 포함하지 않아요.
    search = lambda question, category=None: exact_rows(question, chunks, vectors, model, k=3)
    started = time.perf_counter()
    report = evaluate(dev, search)
    elapsed = time.perf_counter() - started
    results[model_id] = {"dimension": int(vectors.shape[1]), "k": 3,
        "input_format": "passage: +text", "report": report, "query_seconds": elapsed}
    print("[1]", model_id, "dim", vectors.shape[1], "Hit", report["hit_at_k"], "Recall", report["recall_at_k"])

# %% 2. 평균 뒤의 질문별 결과
# 평균 점수가 같아도 틀린 질문이 다를 수 있으므로 질문별 원문 ID와 Recall을 확인해요.
# 전체 결과를 dense_baseline.json에 저장해 이후 개선 결과와 대조할 수 있어요.
for row in results[MODEL_ID]["report"]["rows"]:
    print("[2]", row["question_id"], row["retrieved_document_ids"], row["recall"])
Path("dense_baseline.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print("[3] base", "실행" if args.compare_base else "미실행 (--compare-base로 추가 실행)")
