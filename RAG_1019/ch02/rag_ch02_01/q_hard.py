# -*- coding: utf-8 -*-
# 2장 1강 퀴즈: PDF 본문을 규정 문장으로 복원하기 (Hard: 교안의 TODO를 직접 완성해요)
# 이 폴더에서 uv run q_hard.py로 실행해요.
# main.py를 먼저 실행해 page_text, travel를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from RAG_1019.ch02.rag_ch02_01.main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# PDF의 줄 구조를 확인한 뒤 제목과 꼬리말을 제외하고 본문을 연결하는 과제예요.
# 위치에 따라 자르는 규칙은 이 예제에 맞는지 먼저 확인하세요.
lines = [line.strip() for line in page_text.splitlines() if line.strip()]
# TODO: 제목과 하단 표기를 제외하세요.          -> body_lines
# TODO: 본문 줄을 한 칸의 공백으로 연결하세요.   -> pdf_body
# TODO: 첫 문장과 마지막 문장을 출력하세요.


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("원문과 같은 본문:", pdf_body == travel["content"])
assert body_lines[0].startswith("국내 출장 숙박 비용"), "제목 줄이 본문에 남았어요."
assert not body_lines[-1].startswith("교육용 가상 규정"), "하단 표기가 본문에 남았어요."
assert pdf_body == travel["content"]
print("\n✅ 정답이에요!")
print("생각해 보기:", "모든 PDF에 lines[1:-1]을 적용해도 되는지, 원본 배치를 근거로 토론해 보세요.")
