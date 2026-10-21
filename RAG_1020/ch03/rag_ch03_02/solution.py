# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *

# 각 조각에 문자 수와 E5 최종 입력 토큰 수를 나란히 기록해요.
# 최대 토큰 수를 비교하면 어떤 분할 방식이 입력 한도에 더 가까운지 알 수 있어요.
def measure_chunks(pieces, tokenizer):
    return [{"text": text, "chars": len(text),
             "input_tokens": len(tokenizer("passage: " + text)["input_ids"])}
            for text in pieces]

print("fixed 최대 토큰:", max(r["input_tokens"] for r in measure_chunks(fixed, tokenizer)))
print("token 최대 토큰:", max(r["input_tokens"] for r in measure_chunks(token_chunks, tokenizer)))
