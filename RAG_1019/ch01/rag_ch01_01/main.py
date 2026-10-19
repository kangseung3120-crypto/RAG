# -*- coding: utf-8 -*-
# 수정본 VER 2: 1장 1강 기본 예제
# rag_ch01_01 폴더에서 uv run main.py로 실행하세요.
# 접기 안의 추가 확인과 TODO 문제는 본문 안내에 따라 별도로 덧붙이세요.

import json
from pathlib import Path

# 문서 한 건은 document_id, content, metadata를 가진 딕셔너리예요.
# JSON 파일을 UTF-8로 읽은 뒤 Python 목록으로 바꿔요. 실습 폴더에서 실행해야 상대 경로가 맞아요.
documents = json.loads(Path("documents.json").read_text(encoding="utf-8"))
# 현재 적용되는 규정만 검색 후보로 남겨요. 제목이 비슷해도 폐기된 규정을 섞으면 답이 달라질 수 있어요.
current = [d for d in documents if d["metadata"]["status"] == "current"]
print("전체 문서:", len(documents))
print("현행 문서:", len(current))

# 같은 출장 규정의 현재본과 과거본을 나란히 읽어요.
# 본문의 금액뿐 아니라 status도 함께 확인해야 최신 규정을 구분할 수 있어요.
for doc in documents:
    if doc["document_id"] in {"travel", "travel-old"}:
        print(doc["document_id"], doc["metadata"]["status"])
        print(doc["content"])

# 이 단계는 문자열이 그대로 포함되는지 검사하는 단순 검색이에요.
# 뜻이 비슷한 호텔비와 숙박 비용도 글자가 다르면 검색 결과가 달라져요.
for term in ["숙박 비용", "호텔비", "개인 취미"]:
    found = [d for d in current if term in d["content"]]
    print(term, "->", [d["document_id"] for d in found])

# 검색한 본문을 Context로 묶고 원문 ID를 앞에 붙여 출처를 남겨요.
# replace는 화면에서 문장별로 읽기 쉽게 줄바꿈만 넣는 처리예요.
question = "출장 숙박 비용은 얼마까지 정산되나요?"
found = [d for d in current if "숙박 비용" in d["content"]]
context = "\n".join(
    f"[{d['document_id']}]\n" + d["content"].replace(". ", ".\n")
    for d in found
)
# 질문과 근거를 하나의 프롬프트로 조립해 입력 구조를 확인해요.
# 여기서는 문자열만 출력하며 생성 모델을 호출하거나 실제 답변을 만들지는 않아요.
prompt = (
    "문서를 근거로 질문에 답하세요. 근거가 없으면 확인 불가라고 답하세요.\n"
    + context + "\n질문: " + question
)
print(prompt)
