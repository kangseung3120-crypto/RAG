# -*- coding: utf-8 -*-
# 2장 4강 퀴즈: 파일을 행 단위로 읽는 함수 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 inspect_line, Path (documents.jsonl은 main.py가 만들어요)를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from RAG_1019.ch02.rag_ch02_04.main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 파일을 한 줄씩 읽으면서 1부터 시작하는 줄 번호를 검사 함수에 전달해요.
# 문제가 있는 줄을 조용히 버리지 않고 inspect_line이 원인을 알리게 해요.
def load_jsonl(path):
    result = []
    with Path(path).open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            result.append(inspect_line(line, number))
    return result


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
loaded = load_jsonl("documents.jsonl")
print("마지막 문서:", loaded[-1]["document_id"], loaded[-1]["metadata"]["title"])
assert len(loaded) == 12
assert (loaded[-1]["document_id"], loaded[-1]["metadata"]["title"]) == ("retention", "교육 자료 보관")

# 복사본의 3행 content를 숫자로 바꾸면 3행 오류가 나야 해요.
import json, tempfile, os
rows = Path("documents.jsonl").read_text(encoding="utf-8").splitlines()
broken = json.loads(rows[2]); broken["content"] = 123
rows[2] = json.dumps(broken, ensure_ascii=False)
with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".jsonl", delete=False) as tmp:
    tmp.write("\n".join(rows) + "\n")
try:
    load_jsonl(tmp.name)
    raise AssertionError("3행에서 오류가 나야 해요.")
except ValueError as error:
    print("복사본 오류:", error)
    assert str(error) == "3행: content는 문자열이어야 합니다"
finally:
    os.remove(tmp.name)
print("\n✅ 정답이에요!")
print("생각해 보기:", "오류 행을 조용히 건너뛰지 않고 행 번호와 함께 멈추는 이유를 설명해 보세요.")
