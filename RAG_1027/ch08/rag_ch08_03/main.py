"""8-3: 실제 검색 Context와 수동 주장 검토; --ragas는 모델 연결 필요."""
import argparse
import json
from pathlib import Path
from rag_core import bm25, build_context

parser = argparse.ArgumentParser()
parser.add_argument("--ragas", action="store_true")
args = parser.parse_args()
# BM25로 실제 근거를 검색한 뒤 같은 질문과 Context에 세 답변을 놓고 비교해요.
# 아래 A/B/C 문장은 평가 차이를 보여 주기 위해 사람이 작성한 예시예요.
chunks = json.loads(Path("chunks.json").read_text(encoding="utf-8"))
current = [c for c in chunks if c["metadata"]["status"] == "current"]
golden = [json.loads(s) for s in Path("golden.jsonl").read_text(encoding="utf-8").splitlines()]
item = next(g for g in golden if g["question_id"] == "q05")
hits = bm25(item["question"], current, k=3)
context, sources = build_context(hits)
print("STEP1", [(r["document_id"], r["start"]) for r in hits])
print(context)
# A는 숙박 한도와 증빙을 답하고, B는 금액을 바꾸며, C는 다른 주제의 사실을 답해요.
# 사실성과 질문 관련성을 나눠 평가해야 하는 이유를 보여 줘요.
answers = {
    "A": "숙박비는 1박당 12만원까지이며 숙박 영수증을 첨부해야 합니다.",
    "B": "숙박비는 1박당 30만원까지이며 숙박 영수증을 첨부해야 합니다.",
    "C": "국내 출장 식비는 1일 3만원까지 영수증으로 정산합니다.",
}
# manual의 True/False는 직접 검토한 주장 라벨이에요.
# 이 비율은 라벨을 집계한 수업용 계산이며 RAGAS가 측정한 점수가 아니에요.
manual = {"A": [True, True], "B": [False, True], "C": [True]}
print("STEP2 수동검토 비율", {k: sum(v)/len(v) for k, v in manual.items()})
print("STEP3 질문의 두 요구", ["숙박 한도", "필요한 증빙"])
print("A 두 요구 충족; B 한도 오류; C 한도와 증빙에 답하지 않음")
# 실제 검색 Context와 예시 답변을 파일로 남겨 자동 평가가 같은 입력을 사용하게 해요.
# generated_by_model=False로 답변의 작성 방식을 명시해요.
Path("answer_review_08.json").write_text(json.dumps({
    "question_id": item["question_id"], "question": item["question"], "reference": item["reference"],
    "retrieved_contexts": [r["text"] for r in hits], "answers": answers,
    "manual_labels": manual, "generated_by_model": False}, ensure_ascii=False, indent=2), encoding="utf-8")

# --ragas를 지정하면 run_ragas.py --execute로 연결되어 실제 평가 LLM을 호출해요.
# 옵션 없이 실행하면 수동 검토와 입력 파일 생성까지만 진행해요.
if args.ragas:
    import subprocess
    import sys
    subprocess.run([sys.executable, str(Path(__file__).with_name("run_ragas.py")), "--execute"], check=True)
else:
    print("RAGAS_NOT_RUN: 위 비율은 실습용 라벨의 계산 결과입니다.")
