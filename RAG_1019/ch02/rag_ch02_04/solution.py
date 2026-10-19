# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from RAG_1019.ch02.rag_ch02_04.main import *

# 파일을 한 줄씩 읽으면서 1부터 시작하는 줄 번호를 검사 함수에 전달해요.
# 문제가 있는 줄을 조용히 버리지 않고 inspect_line이 원인을 알리게 해요.
def load_jsonl(path):
    result = []
    with Path(path).open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            result.append(inspect_line(line, number))
    return result

loaded = load_jsonl("documents.jsonl")
print("마지막 문서:", loaded[-1]["document_id"], loaded[-1]["metadata"]["title"])
