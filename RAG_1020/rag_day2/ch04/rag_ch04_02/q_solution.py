# -*- coding: utf-8 -*-
# 4장 2강 퀴즈: 손계산 결과와 검색 코드를 맞추기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 np를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 후보별 길이는 행마다 구하므로 axis=1, 높은 점수부터 정렬하려고 점수에 마이너스를 붙여요.
q = np.array([1., 0.])
candidates = np.array([[1., 1.], [3., 0.], [-1., 0.]])
lengths = np.linalg.norm(candidates, axis=1)
scores = (candidates @ q) / (lengths * np.linalg.norm(q))
order = np.argsort(-scores)
print(scores.round(4).tolist())
print(order.tolist())


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert scores.round(4).tolist() == [0.7071, 1.0, -1.0]
assert order.tolist() == [1, 0, 2], "높은 점수부터 정렬했는지 확인하세요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "'호텔비 지원 한도는?'처럼 표현을 바꾼 질문으로 상위 3개 원문을 읽고, 정답 조건이 포함됐는지 한 문장으로 적어 보세요.")
