# -*- coding: utf-8 -*-
# 수정본 VER 2: 1장 2강 기본 예제
# rag_ch01_02 폴더에서 uv run main.py로 실행하세요.
# 접기 안의 추가 확인과 TODO 문제는 본문 안내에 따라 별도로 덧붙이세요.

import json
import re
from pathlib import Path
from collections import defaultdict

# 현재 규정 중 출장 문서를 골라 단어 목록을 살펴봐요.
# 정규식은 한글, 영문, 숫자의 연속 구간을 추출하며 한국어 형태소 분석은 하지 않아요.
documents = json.loads(Path("documents.json").read_text(encoding="utf-8"))
current = [d for d in documents if d["metadata"]["status"] == "current"]
travel = next(d for d in current if d["document_id"] == "travel")
words = re.findall(r"[가-힣a-zA-Z0-9]+", travel["content"])
print(words[:10])

# 단어를 키로, 그 단어가 등장한 문서 ID 집합을 값으로 저장하는 역색인이에요.
# 문서 한 곳에 단어가 여러 번 나와도 set 덕분에 같은 ID는 한 번만 저장돼요.
def build_index(docs):
    postings = defaultdict(set)
    for doc in docs:
        for word in re.findall(r"[가-힣a-zA-Z0-9]+", doc["content"]):
            postings[word].add(doc["document_id"])
    return dict(postings)

# 색인은 문서를 읽을 때 한 번 만들고 여러 질문에서 재사용할 수 있어요.
# 정렬은 출력 순서를 고정하기 위한 것이며 검색 점수 순위는 아니에요.
index = build_index(current)
for word in ["숙박", "영수증을", "재택근무는"]:
    print(word, "->", sorted(index.get(word, set())))

# 질문의 단어별 문서 ID를 합집합으로 모아요. 한 단어만 일치해도 후보가 되는 OR 검색이에요.
# 이 예제에는 관련도 점수나 동의어 처리가 없으므로 반환값은 후보 ID 목록이에요.
def search_words(query, index):
    words = re.findall(r"[가-힣a-zA-Z0-9]+", query)
    ids = set()
    for word in words:
        ids.update(index.get(word, set()))
    return sorted(ids)

# 색인은 문서 ID만 돌려주므로 ID → 원문 조회표로 제목과 본문을 복원해요.
by_id = {d["document_id"]: d for d in current}
for did in search_words("숙박 영수증을", index):
    print(did, by_id[did]["metadata"]["title"])
    print(by_id[did]["content"].split(". ")[0])

# 원문에 문서를 추가해도 이미 만든 색인은 자동으로 갱신되지 않아요.
# 새 색인과 옛 색인의 결과를 비교해 Indexing을 다시 해야 하는 이유를 확인해요.
before = build_index([d for d in current if d["document_id"] != "remote"])
after = build_index(current)
print("추가 전:", search_words("재택근무는", before))
print("추가 후:", search_words("재택근무는", after))
print("기존 인덱스:", search_words("재택근무는", before))
