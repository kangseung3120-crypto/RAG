# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *

# 겹침이 크기 이상이면 이동 간격이 0 이하가 되므로 실행 전에 막아요.
# 본문을 자르는 로직은 windows를 그대로 재사용해 검증과 분할의 역할을 나눠요.
def checked_windows(text, size, overlap):
    if not 0 <= overlap < size:
        raise ValueError("0 <= overlap < size")
    return windows(text, size, overlap)

for start, end, piece in checked_windows(text, 100, 20):
    print(f"[{start}:{end}]", piece)
