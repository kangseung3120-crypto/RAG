# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# 중복 질의는 검색 전에 제거해 같은 BM25 계산을 반복하지 않아요.
# all_rows에는 서로 다른 질의가 반환한 중복 청크가 아직 남을 수 있어요.
queries = [question, variants[1], variants[1], variants[2]]
unique_queries = list(dict.fromkeys(queries))
all_rows = []
for query in unique_queries: all_rows.extend(bm25(query, current, k=3))
print("검색 횟수:", len(unique_queries))
print("반환 청크 수:", len(all_rows))
