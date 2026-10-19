# -*- coding: utf-8 -*-
# 2장 2강 퀴즈: 현행 출장 문서만 고르기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 documents, source_label를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 업무 범주와 현재 적용 상태를 모두 만족하는 문서만 선택해요.
# 같은 범주의 과거 문서를 제외한 뒤에도 원문 출처는 그대로 유지돼요.
def choose_current(docs, category):
    return [d for d in docs if d["metadata"]["category"] == category
            and d["metadata"]["status"] == "current"]


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
for doc in choose_current(documents, "출장"):
    print(doc["document_id"], source_label(doc))
print("교육:", [d["document_id"] for d in choose_current(documents, "교육")])

assert [d["document_id"] for d in choose_current(documents, "출장")] == ["travel", "meal"]
assert [d["document_id"] for d in choose_current(documents, "교육")] == ["education"]
assert choose_current(documents, "출장")[0] is next(d for d in documents if d["document_id"] == "travel"), \
    "새 dict를 만들지 말고 원래 문서 객체를 반환하세요."
print("\n✅ 정답이에요!")
print("생각해 보기:", "travel-old가 빠지는 이유와 travel·meal이 함께 선택되는 이유를 필드 값으로 설명해 보세요.")
