# -*- coding: utf-8 -*-
# 2장 1강 퀴즈: PDF 본문을 규정 문장으로 복원하기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 page_text, travel를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from RAG_1019.ch02.rag_ch02_01.main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 빈 줄을 제외하고 예제 PDF의 첫 줄 제목과 마지막 줄 꼬리말을 분리해요.
# lines[1:-1]은 이 PDF의 구조를 확인한 뒤 쓰는 규칙이며 모든 PDF에 적용하는 규칙은 아니에요.
lines = [line.strip() for line in page_text.splitlines() if line.strip()]
body_lines = lines[1:-1]
pdf_body = " ".join(body_lines)
print("제목:", lines[0])
print("첫 문장:", pdf_body.split(". ")[0])
print("마지막 문장:", pdf_body.split(". ")[-1])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("원문과 같은 본문:", pdf_body == travel["content"])
assert body_lines[0].startswith("국내 출장 숙박 비용"), "제목 줄이 본문에 남았어요."
assert not body_lines[-1].startswith("교육용 가상 규정"), "하단 표기가 본문에 남았어요."
assert pdf_body == travel["content"]
print("\n✅ 정답이에요!")
print("생각해 보기:", "모든 PDF에 lines[1:-1]을 적용해도 되는지, 원본 배치를 근거로 토론해 보세요.")
