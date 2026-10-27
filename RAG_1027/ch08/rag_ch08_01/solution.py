# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# q09의 참고 답변을 정답 문서 원문과 대조해요.
# 금액만 일치하는지 보지 말고 대상, 단위, 예외 조건까지 확인하세요.
target_id = "q09"
target = next(g for g in golden if g["question_id"] == target_id)
for did in target["relevant_document_ids"]:
    source = by_id[did]
    print(source["metadata"]["title"])
    print(source["content"])
