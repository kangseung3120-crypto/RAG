# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# main.py에서 닫은 색인은 다시 쓸 수 없어 새 DenseIndex를 만들어요.
# q10의 교육 규정 청크를 직접 읽어 질문에 필요한 서류가 어느 위치에 있는지 확인해요.
dense = DenseIndex(chunks)
try:
    question = next(g["question"] for g in golden if g["question_id"] == "q10")
    for row in dense.search(question, k=6):
        if row["document_id"] == "education": print(row["start"], row["text"])
finally:
    dense.close()
