# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# 같은 질의를 반복한 경우와 표현을 바꾼 경우를 동일한 검색 한도에서 비교해요.
# 상태, 시도 수, 청크 위치를 함께 읽어 재검색의 효과를 확인해요.
same = [question, question]
changed = [question, "교육비 지원 수강 완료 후 제출합니다"]
for items in [same, changed]:
    rows, trace, status = search_loop(items, "교육비", max_searches=2)
    print(status, len(trace), [c["start"] for c in rows])
