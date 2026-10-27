# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# 저장된 dev 결과에서 q10을 찾아 평균 뒤에 숨은 개별 실패를 확인해요.
# 검색 문서 ID를 원문과 대조한 뒤 청킹, 질의 표현, 후보 수 중 어느 단계가 원인인지 판단하세요.
saved = json.loads(Path("comparison_08.json").read_text(encoding="utf-8"))
hybrid_rows = saved["dev"]["hybrid"]["rows"]
q10 = next(r for r in hybrid_rows if r["question_id"] == "q10")
print(q10["retrieved_document_ids"], q10["recall"])
