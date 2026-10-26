"""7-3: 실제 다국어 CrossEncoder의 질문-청크 쌍 점수."""
import argparse
import json
import os
from pathlib import Path
from rag_core import reciprocal_rank_fusion

# --skip-model은 후보 구성만 확인하고 실제 재정렬 모델 실행을 생략해요.
# 기본 실행은 모델을 내려받아 CPU에서 질문-청크 쌍을 함께 평가해요.
parser = argparse.ArgumentParser()
parser.add_argument("--skip-model", action="store_true")
parser.add_argument("--model", default="cross-encoder/mmarco-mMiniLMv2-L12-H384-v1")
args = parser.parse_args()
# RRF로 넓게 모은 후보에 동일 질문을 각각 짝지어요.
# CrossEncoder는 이 쌍을 함께 읽으므로 문서 벡터를 미리 계산하는 Dense 검색과 계산 구조가 달라요.
runs = json.loads(Path("search_runs_07.json").read_text(encoding="utf-8"))
run = next(r for r in runs if r["question_id"] == "q06")
candidates = reciprocal_rank_fusion([run["bm25"], run["dense"]], k=8)
pairs = [(run["question"], c["text"]) for c in candidates]
print("STEP1", "후보", len(candidates), "점수화할 쌍", len(pairs))
print("첫 후보", candidates[0]["document_id"], candidates[0]["start"])
print("질문:", pairs[0][0])
print("본문:", pairs[0][1])
print("STEP2", [(n, len(pairs[:n])) for n in [2, 4, 8]])
if args.skip_model:
    print("MODEL_NOT_RUN: 후보와 입력 쌍만 확인했습니다.")
else:
    import torch
    from sentence_transformers import CrossEncoder
    # Identity를 사용해 원래 logit을 받아요. 값이 음수이거나 1을 넘어도 확률 오류가 아니에요.
    # max_length=256이므로 질문과 본문을 합친 길이가 이 한도를 넘는지 다음 출력에서 확인하세요.
    model = CrossEncoder(args.model, device="cpu", max_length=256,
                         activation_fn=torch.nn.Identity(),
                         cache_folder=os.environ.get("RAG_MODEL_CACHE"))
    lengths = [len(model.tokenizer(q, text)["input_ids"]) for q, text in pairs]
    print("PAIR_TOKENS", lengths)
    # 네 쌍씩 묶어 추론한 뒤 높은 점수부터 재정렬해요.
    # 기존 후보 위치 i와 새 순위를 함께 남겨 어느 근거가 올라오고 내려갔는지 확인해요.
    values = model.predict(pairs, batch_size=4, show_progress_bar=False)
    order = sorted(range(len(values)), key=lambda i: (-float(values[i]), candidates[i]["chunk_id"]))
    print("STEP3", "model", args.model)
    for rank, i in enumerate(order, 1):
        c = candidates[i]
        print(rank, c["document_id"], c["start"], "이전", i+1, "logit", round(float(values[i]), 4))
    # 새 순위와 옛 순위를 파일로 저장해 재정렬의 효과를 질문별로 대조할 수 있게 해요.
    rows = [{"chunk_id": candidates[i]["chunk_id"], "old_rank": i+1,
             "new_rank": rank, "score": float(values[i])}
            for rank, i in enumerate(order, 1)]
    Path("rerank_07.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")