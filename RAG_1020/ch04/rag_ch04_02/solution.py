# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *

#  정렬 방향
# 코사인 유사도는 클수록 가깝고 1 - 유사도로 만든 거리는 작을수록 가까워요.
# 정렬 방향을 반대로 적용해도 두 결과의 문서 순서가 같은지 확인해요.
distance = 1 - cosines
print("[4] similarity order", np.argsort(-cosines).tolist())
print("distance order", np.argsort(distance).tolist())
