# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from RAG_1019.ch02.rag_ch02_02.main import *

# 업무 범주와 현재 적용 상태를 모두 만족하는 문서만 선택해요.
# 같은 범주의 과거 문서를 제외한 뒤에도 원문 출처는 그대로 유지돼요.
def choose_current(docs, category):
    return [d for d in docs if d["metadata"]["category"] == category
            and d["metadata"]["status"] == "current"]

for doc in choose_current(documents, "출장"):
    print(doc["document_id"], source_label(doc))
