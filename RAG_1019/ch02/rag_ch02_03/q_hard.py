# -*- coding: utf-8 -*-
# 2장 3강 퀴즈: 지운 줄도 함께 반환하기 (Hard: 교안의 TODO를 직접 완성해요)
# 이 폴더에서 uv run q_hard.py로 실행해요.
# main.py를 먼저 실행해 lines (PDF 줄 목록), re를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from RAG_1019.ch02.rag_ch02_03.main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 빈 줄과 지정한 꼬리말만 제거하며 남긴 줄과 제거한 줄을 함께 반환해요.
# 문장 내용을 임의로 요약하지 않아 정제 전후의 의미를 직접 대조할 수 있어요.
def clean_lines(text, footer):
    kept, removed = [], []
    for line in text.splitlines():
    # TODO: 줄마다 연속 공백/탭을 정리하세요.
        value = re.sub(r"[ \t]+", " ", line).strip()
    # TODO: 빈 줄 또는 footer와 같은 줄을 removed에 모으세요.
        if not value or value == footer:
            removed.append(line)
        else:
            kept.append(value)
    # TODO: 나머지는 줄바꿈으로 연결해 반환하세요.
    return "\n".join(kept), removed


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
# 이 예제에서는 실제 마지막 줄을 footer로 넘겨요. 파일마다 꼬리말 구조를 먼저 확인하세요.
clean, removed = clean_lines("\n".join(lines), lines[-1])
print(clean)
print("제외한 줄:", removed)

assert removed == [lines[-1]]
assert clean.splitlines()[0] == "출장 숙박 정산", "제목 줄은 그대로 둬요."
assert len(clean.splitlines()) == 4, "줄바꿈을 유지해야 해요."
for phrase in ["12만원", "예약 전에", "정산되지 않습니다"]:
    assert phrase in clean, phrase
clean2, removed2 = clean_lines("  출장\t\t숙박  \n\n교육용 꼬리말", "다른 꼬리말")
assert clean2 == "출장 숙박\n교육용 꼬리말" and removed2 == [""]
print("\n✅ 정답이에요!")
print("생각해 보기:", "footer에 다른 문자열을 넘기면 어떤 줄이 유지되는지 비교해 보세요.")
