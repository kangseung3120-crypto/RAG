# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *

# 빈 줄과 지정한 꼬리말만 제거하며 남긴 줄과 제거한 줄을 함께 반환해요.
# 문장 내용을 임의로 요약하지 않아 정제 전후의 의미를 직접 대조할 수 있어요.
def clean_lines(text, footer):
    kept, removed = [], []
    for line in text.splitlines():
        value = re.sub(r"[ \t]+", " ", line).strip()
        if not value or value == footer:
            removed.append(line)
        else:
            kept.append(value)
    return "\n".join(kept), removed

# 이 예제에서는 실제 마지막 줄을 footer로 넘겨요. 파일마다 꼬리말 구조를 먼저 확인하세요.
clean, removed = clean_lines("\n".join(lines), lines[-1])
print(clean)
print("제외한 줄:", removed)
