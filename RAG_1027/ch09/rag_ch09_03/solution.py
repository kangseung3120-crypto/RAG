# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# 팀장으로 들어오는 규정 간선을 따라 승인 시점과 원문 ID를 확인해요.
# 같은 승인자라는 이유만으로 서로 다른 규정의 조건을 하나로 합치지 않아요.
policies = sorted(graph.predecessors("팀장"))
for did in policies:
    edge = graph[did]["팀장"]
    print(did, edge["condition"], edge["source_document_id"])
