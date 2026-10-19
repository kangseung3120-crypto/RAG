import json
from pathlib import Path


documents = json.loads(Path("documents.json").read_text(encoding="utf-8"))


current = [d for d in documents
if d ["metadata"]["status"]
=="current"]

print("전체 문서:", len(documents))
print("현행 문서:", len(current))

for doc in documents:
    if doc["document_id"] in {"travel", "travel-old"}:
        print(doc["document_id"], doc["metadata"]["status"])
        print(doc["content"])

for term in ["숙박 비용", "호텔비", "개인 취미"]:
    found = [d for d in current
             if term in d["content"]]
    print(term, "->",
           [d["document_id"]for d in found]) 

question = "출장 숙박 비용은 얼마까지 정산되나요?"
und = [d for d in current if "숙박 비용" in d["content"]]
context = "\n".join(
    f"[{d['document_id']}]\n" + d["content"].replace(". ", ".\n")
    for d in found    
)

prompt = (
    "문서를 근거로 질문에 답하세요. 근거가 없으면 확인 불가라고 답하세요.\n"
    + context + "\n질문: " + question
)

print(prompt)
                               