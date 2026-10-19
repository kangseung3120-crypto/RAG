# %% inspect
import json
import hashlib
from pathlib import Path
from copy import deepcopy

# 현재본과 과거본의 ID, 버전, 발행일, 상태를 함께 읽어요.
# 발행일 하나만으로 최신 규정을 판단하지 않고 적용 상태도 확인해요.
documents = json.loads(Path("documents.json").read_text(encoding="utf-8"))
travel = next(d for d in documents if d["document_id"] == "travel")
old = next(d for d in documents if d["document_id"] == "travel-old")
for doc in [travel, old]:
    print(doc["document_id"], doc["metadata"]["version"],
          doc["metadata"]["published_at"], doc["metadata"]["status"])

# %% citation
# 사용자가 원문으로 돌아갈 수 있도록 제목, 버전, URL을 하나의 출처 표기로 묶어요.
# URL은 본문 검색 점수를 높이기 위한 값이 아니라 출처 추적에 쓰는 값이에요.
def source_label(doc):
    meta = doc["metadata"]
    return f"{meta['title']} ({meta['version']}) | {meta['source_url']}"

print(source_label(travel))
print(source_label(old))

# %% copy
# 청크마다 section을 달리 붙이기 전에 메타데이터를 깊게 복사해요.
# 중첩된 값까지 분리되므로 한 청크의 수정이 원문이나 다른 청크로 퍼지지 않아요.
left = deepcopy(travel["metadata"])
right = deepcopy(travel["metadata"])
left["section"] = "숙박 한도"
right["section"] = "한도 초과 승인"
print(left["title"], "->", left["section"])
print(right["title"], "->", right["section"])
print("원문 section:", travel["metadata"].get("section"))

# %% hash
# 본문을 UTF-8 바이트로 바꿔 해시를 계산해요. 본문이 달라지면 재색인이 필요한지 판단할 수 있어요.
# 앞 12자리 표시는 수업에서 비교하기 위한 축약값이며 문서 ID 자체를 대체하지는 않아요.
for doc in [travel, old]:
    digest = hashlib.sha256(doc["content"].encode("utf-8")).hexdigest()[:12]
    print(doc["document_id"], digest, doc["metadata"]["source_url"])
