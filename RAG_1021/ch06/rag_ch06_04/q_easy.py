# -*- coding: utf-8 -*-
# 6장 4강 퀴즈: 부족한 내용을 구체적으로 안내하기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 states, finish를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 범위 밖 질문에 대한 보류 응답을 작성하는 과제예요.
# 상태와 인용을 맞추고 answer에는 확인하지 못한 항목과 추가로 필요한 자료를 구체적으로 적으세요.
target = states[3]
draft = {
    "status": ____,
    "answer": ____,
    "citations": ____,
}
checked = finish({**target, "draft": draft})
print(checked["answer"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("질문:", target["question"])
assert checked["status"] == "insufficient", "근거가 없으니 보류(insufficient)예요"
assert checked["sources"] == [], "보류 응답에는 출처를 달지 않아요"
assert "항공" in checked["answer"] and len(checked["answer"]) >= 20, "무엇이 부족한지 구체적으로 적어요"
assert "12만원" not in checked["answer"], "국내 숙박 규정을 해외 항공 규정으로 확대하지 않아요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "모호한 '지원 한도' 질문(states[5])에는 어떤 비용 항목인지 되묻는 보류 문장을 작성해 finish로 확인해 보세요.")
