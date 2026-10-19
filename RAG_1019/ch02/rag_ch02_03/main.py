# %% whitespace
import json
import re
import unicodedata
from pathlib import Path
from copy import deepcopy

documents = json.loads(Path("documents.json").read_text(encoding="utf-8"))
travel = next(d for d in documents if d["document_id"] == "travel")
# 원래 문장에 공백과 탭을 일부러 더해 정제 전후를 비교해요.
# repr을 쓰면 보이지 않는 탭과 양끝 공백도 출력에서 구분할 수 있어요.
sample = travel["content"].split(". ")[0] + "."
noisy = "  " + sample.replace(" ", "  ") + "\t"
print("정제 전:", repr(noisy))
# NFC로 같은 한글의 유니코드 표현을 맞추고 연속된 공백과 탭만 줄여요.
# 문장의 부정 표현이나 금액처럼 의미가 있는 내용은 바꾸지 않아요.
cleaned = re.sub(r"[ \t]+", " ", unicodedata.normalize("NFC", noisy)).strip()
print("정제 후:", repr(cleaned))

# %% boilerplate
from pypdf import PdfReader

# 먼저 줄 번호와 내용을 출력해 제목과 꼬리말의 위치를 확인해요.
# 아래의 첫 줄과 마지막 줄 제외는 이 예제 PDF 구조에만 맞춘 처리예요.
lines = PdfReader("raw/travel.pdf").pages[0].extract_text().splitlines()
for n, line in enumerate(lines):
    print(n, line)
body = " ".join(line.strip() for line in lines[1:-1])
print("검색용 본문:", body)

# %% duplicates
import hashlib

# 원문을 복사해 중복 사례를 만들어요. 버전, 범주, 본문 해시를 함께 중복 기준으로 써요.
# 본문이 비슷해도 버전이 다르면 보존할 수 있도록 본문만으로 삭제하지 않아요.
trial = documents + [deepcopy(travel)]
seen, unique, excluded = set(), [], []
for doc in trial:
    key = (doc["metadata"]["version"], doc["metadata"]["category"],
           hashlib.sha256(doc["content"].encode("utf-8")).hexdigest())
    # 이미 처리한 키는 excluded에 남기고 다음 문서로 넘어가요.
    # 제외 기록이 있어야 필요한 규정을 실수로 지우지 않았는지 검수할 수 있어요.
    if key in seen:
        excluded.append(doc["document_id"])
        continue
    seen.add(key)
    unique.append(doc)
print("입력", len(trial), "유지", len(unique), "중복 제외", excluded)
print("숙박 규정:", [d["document_id"] for d in unique if d["document_id"].startswith("travel")])

# %% meaning
# 정제 과정에서 부정어를 없애면 규정의 뜻이 반대로 바뀌어요.
# 아래 출력은 잘못된 변환을 보여 주는 예시이며 원본 documents를 수정하지 않아요.
sentence = next(s for s in travel["content"].split(". ") if "자동 정산" in s)
print("보존할 문장:", sentence)
print("잘못 바꾼 결과:", sentence.replace("자동 정산되지 않습니다", "자동 정산됩니다"))


# %% empty_document
# 공백만 있는 가짜 문서를 추가해 빈 본문 검사가 작동하는지 확인해요.
# strip 후 빈 문자열이면 검색용 자료에서 제외하고 원인을 기록해요.
blank_doc = deepcopy(travel)
blank_doc["document_id"] = "blank-demo"
blank_doc["content"] = " \n\t"
checked, rejected = [], []
for doc in documents + [blank_doc]:
    if not doc["content"].strip():
        rejected.append((doc["document_id"], "빈 본문"))
    else:
        checked.append(doc)
print("빈 본문 검사:", len(checked), "개 유지", rejected)
