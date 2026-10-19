# %% serialize
import json
from pathlib import Path

# Python 딕셔너리를 JSON 문자열로 직렬화해 저장 가능한 형태로 바꿔요.
# ensure_ascii=False는 한국어를 읽을 수 있는 글자로 남기는 옵션이에요.
documents = json.loads(Path("documents.json").read_text(encoding="utf-8"))
row = documents[3]
packed = json.dumps(row, ensure_ascii=False)
print(packed)
print("Python 본문 시작:", row["content"][:45])

# %% write
# JSONL은 한 줄에 JSON 객체 하나를 저장해요. 파일을 w 모드로 열면 기존 출력은 덮어써요.
# 문서별로 dumps를 호출하고 마지막에 줄바꿈을 하나씩 추가해 레코드 경계를 구분해요.
target = Path("documents.jsonl")
with target.open("w", encoding="utf-8", newline="\n") as stream:
    for doc in documents:
        stream.write(json.dumps(doc, ensure_ascii=False) + "\n")

# 저장한 파일을 다시 읽고 줄마다 JSON 객체로 복원해요.
# 입력 문서 수와 복원된 문서 수가 같은지, ID와 제목이 유지됐는지 확인해요.
loaded = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines()]
print("저장 문서:", len(loaded))
for doc in loaded[:3]:
    print(doc["document_id"], doc["metadata"]["title"])

# %% linebreak
# 본문 안의 줄바꿈은 JSON 문자열 안에서 이스케이프되므로 JSONL 레코드가 여러 줄로 갈라지지 않아요.
# json.loads를 거치면 본문에는 실제 줄바꿈이 복원돼요.
display_copy = dict(row)
display_copy["content"] = row["content"].replace(". ", ".\n")
one_line = json.dumps(display_copy, ensure_ascii=False)
print("JSONL 본문 부분:", one_line[one_line.index('"content"'):][:100])
restored = json.loads(one_line)
print("다시 읽은 본문:")
print(restored["content"])

# %% errors
# 문법 검사 다음에 레코드가 객체인지, content가 문자열인지 확인해요.
# 오류를 줄 번호와 함께 다시 올려야 큰 파일에서도 문제가 난 위치를 찾을 수 있어요.
def inspect_line(line, number):
    try:
        obj = json.loads(line)
        if not isinstance(obj, dict):
            raise ValueError("각 행은 JSON 객체여야 합니다")
        if not isinstance(obj.get("content"), str):
            raise ValueError("content는 문자열이어야 합니다")
        return obj
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"{number}행: {error}") from error

# 숫자 본문과 빈 줄을 일부러 넣은 오류 사례예요.
# 에러가 출력돼도 바깥 try/except가 처리하므로 두 사례를 모두 확인할 수 있어요.
for number, line in [(2, '{"content": 123}'), (3, '')]:
    try:
        inspect_line(line, number)
    except ValueError as error:
        print(error)
