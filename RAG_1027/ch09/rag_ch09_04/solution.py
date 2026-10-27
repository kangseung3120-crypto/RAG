# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# 계산에 사용한 금액과 원문 ID, URL을 함께 출력해 숫자의 출처를 확인해요.
# 계산 결과에도 근거를 연결해야 다른 규정의 금액을 잘못 사용한 문제를 찾을 수 있어요.
chosen = next(r for r in rows if r["document_id"] == "travel")
print(chosen["limit_won"], chosen["document_id"], chosen["source_url"])
