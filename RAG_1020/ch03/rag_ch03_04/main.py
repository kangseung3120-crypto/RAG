# %% corpus
import json
from pathlib import Path
from rag_core import chunk_documents

# 비교에 사용할 근거 문장을 먼저 고정해요. 청킹 조건을 바꾼 뒤 기준을 바꾸면 공정한 비교가 어려워요.
documents = [json.loads(line) for line in Path("documents.jsonl").read_text(encoding="utf-8").splitlines()]
travel = next(d for d in documents if d["document_id"] == "travel")
evidence = [s + "." for s in travel["content"].split(". ")[:3]]
for n, phrase in enumerate(evidence, 1):
    print(n, len(phrase), phrase)

# %% compare
# 동일한 자료에 크기와 겹침만 바꿔 적용해요. kept는 각 근거 문장이 한 청크 안에 온전히 남는지예요.
# 이 값은 근거 보존 검사이며 실제 검색 성능이나 답변 정확도 점수는 아니에요.
for size, overlap in [(80, 0), (80, 20), (100, 20)]:
    chunks = chunk_documents(documents, size=size, overlap=overlap)
    selected = [c for c in chunks if c["document_id"] == "travel"]
    kept = [any(phrase in c["text"] for c in selected) for phrase in evidence]
    print(size, overlap, "전체 청크", len(chunks), "travel", len(selected),
          "저장 문자", sum(len(c["text"]) for c in selected), "근거 보존", kept)

# %% inspect
# 시작점과 끝점을 원문과 대조해 문장이나 예외 조건이 경계에서 끊기는지 읽어 보세요.
for row in chunk_documents([travel], size=80, overlap=20):
    print(row["start"], row["end"], row["text"])

# %% save
# 선택한 청킹 조건으로 결과를 저장하고 다시 읽어 구조가 유지되는지 확인해요.
# 본문을 수정하거나 청킹 조건을 바꾸면 뒤의 임베딩도 다시 만들어야 해요.
chunks = chunk_documents(documents, size=80, overlap=20)
Path("chunks.json").write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
loaded = json.loads(Path("chunks.json").read_text(encoding="utf-8"))
print("저장한 청크:", len(loaded))
print(json.dumps(loaded[0], ensure_ascii=False, indent=2))
