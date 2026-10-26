# -*- coding: utf-8 -*-
# 6장 3강 퀴즈: 맞는 바꿔쓰기와 틀린 바꿔쓰기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 lookup, bind_claim, quote를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 두 문장 모두 인용문과 표현이 달라 review_meaning으로 남아요.
texts = [
    "국내 출장의 숙박비 한도는 1박 기준 12만원입니다.",
    "국내 출장의 숙박비 한도는 전체 일정 기준 12만원입니다.",
]
statuses = []
for text in texts:
    candidate = {
        "source_id": "S1",
        "text": text,
        "quote": quote,
    }
    statuses.append(bind_claim(candidate, lookup)[0])
    print(statuses[-1], text)


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert statuses == ["review_meaning", "review_meaning"], "S1과 원문 발췌 quote를 넣으면 둘 다 review_meaning이에요"
print("코드 결과는 같지만: 첫 문장은 의미 유지(1박 기준), 둘째는 단위 오류(전체 일정)")
print("\n✅ 정답이에요!")
print("생각해 보기:", "receipt_claim의 text를 '영수증을 제출하지 않아도 정산할 수 있어요.'로 바꾸면 코드가 무엇을 감지하고 무엇을 놓치는지 설명해 보세요.")
