"""8-1: 공통 golden20 읽기, 정답 근거와 분할 감사."""
import json
from collections import Counter
from pathlib import Path

# 질문, 정답 문서 ID, 참고 답변, 답변 가능 여부, dev/test 분할을 읽어요.
# 문서 수와 질문 수, 각 분할의 구성을 먼저 확인해 어떤 범위를 평가하는지 파악해요.
docs = json.loads(Path("documents.json").read_text(encoding="utf-8"))
golden = [json.loads(s) for s in Path("golden.jsonl").read_text(encoding="utf-8").splitlines()]
print("STEP1", "문서", len(docs), "질문", len(golden))
print("split", dict(Counter(g["split"] for g in golden)))
print("answerable", dict(Counter(g["answerable"] for g in golden)))
# 정답 문서 ID를 실제 원문에 연결해 참고 답변의 근거가 있는지 읽어요.
# 정답셋도 사람이 만든 자료이므로 검색기 평가 전에 자체 검수가 필요해요.
by_id = {d["document_id"]: d for d in docs}
item = next(g for g in golden if g["question_id"] == "q06")
print("STEP2", item["question"], item["reference"])
for did in item["relevant_document_ids"]:
    print(did, by_id[did]["content"])
# 분할별 근거 문서와 답이 없는 질문 수를 비교해요.
# 질문을 나눴다고 원문까지 분리된 것은 아니므로 아래 문서 교집합도 확인해요.
for split in ["dev", "test"]:
    selected = [g for g in golden if g["split"] == split]
    ids = {did for g in selected for did in g["relevant_document_ids"]}
    print("STEP3", split, "근거문서", sorted(ids),
          "답없음", sum(not g["answerable"] for g in selected))
# dev와 test가 같은 규정을 공유하면 새로운 문서에 대한 일반화 성능으로 해석하기 어려워요.
# 이 출력은 평가셋의 한계를 확인하는 자료이며 점수 자체는 아니에요.
dev_ids = {d for g in golden if g["split"] == "dev" for d in g["relevant_document_ids"]}
test_ids = {d for g in golden if g["split"] == "test" for d in g["relevant_document_ids"]}
print("문서 교집합", sorted(dev_ids & test_ids))
