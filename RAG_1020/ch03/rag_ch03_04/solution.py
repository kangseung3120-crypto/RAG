# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *

# 원문 ID별로 청크의 문자 구간을 모아 겹침과 빈 구간을 살펴볼 수 있게 해요.
# 범위 목록을 출력하는 함수이며 완전한 원문 복원 여부를 자동 판정하지는 않아요.
def coverage_by_document(chunks):
    result = {}
    for c in chunks:
        result.setdefault(c["document_id"], []).append((c["start"], c["end"]))
    return result

for did, ranges in coverage_by_document(chunks).items():
    print(did, ranges)
