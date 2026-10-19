# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *

# 빈 줄을 제외하고 예제 PDF의 첫 줄 제목과 마지막 줄 꼬리말을 분리해요.
# lines[1:-1]은 이 PDF의 구조를 확인한 뒤 쓰는 규칙이며 모든 PDF에 적용하는 규칙은 아니에요.
lines = [line.strip() for line in page_text.splitlines() if line.strip()]
body_lines = lines[1:-1]
pdf_body = " ".join(body_lines)
print("제목:", lines[0])
print("첫 문장:", pdf_body.split(". ")[0])
print("마지막 문장:", pdf_body.split(". ")[-1])
# 정제한 PDF 본문이 기준 문서와 정확히 같은지 비교해 누락을 확인해요.
# False라면 첫 문장과 마지막 문장, 공백, 줄 순서를 차례로 살펴보세요.
print("원문과 같은 본문:", pdf_body == travel["content"])
