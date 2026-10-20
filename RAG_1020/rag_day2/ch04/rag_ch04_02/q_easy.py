# -*- coding: utf-8 -*-
# 4장 2강 퀴즈: 손계산 결과와 검색 코드를 맞추기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 np를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 후보별 길이를 구하는 축과 점수를 높은 순으로 정렬하는 방향을 채워 보세요.
# 숫자가 큰 벡터와 방향이 가까운 벡터를 구분하는 계산 연습이에요.
q = np.array([1., 0.])
candidates = np.array([[1., 1.], [3., 0.], [-1., 0.]])
lengths = candidates @ q
scores = (candidates @ q) / (lengths * np.linalg.norm(q))
order = np.argsort(-scores)
print(scores.round(4).tolist())
print(order.tolist())


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert scores.round(4).tolist() == [0.7071, 1.0, -1.0]
assert order.tolist() == [1, 0, 2], "높은 점수부터 정렬했는지 확인하세요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "'호텔비 지원 한도는?'처럼 표현을 바꾼 질문으로 상위 3개 원문을 읽고, 정답 조건이 포함됐는지 한 문장으로 적어 보세요.")
