# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# 선택한 문장 중 승인 조건이 있는 문장과 원문 위치를 확인해요.
# 압축 뒤 예외 규정이 빠지지 않았는지 검사하는 연습이에요.
chosen = [(start, end, text) for start, end, text in selected if "승인" in text]
for row in chosen: print(row)
