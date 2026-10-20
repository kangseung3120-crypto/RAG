# -*- coding: utf-8 -*-
# 3장 2강 퀴즈: 분할 결과를 한 표로 비교하기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 fixed, recursive, token_chunks, tokenizer를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 각 조각에 문자 수와 E5 최종 입력 토큰 수를 나란히 기록해요.
# 최대 토큰 수를 비교하면 어떤 분할 방식이 입력 한도에 더 가까운지 알 수 있어요.
def measure_chunks(pieces, tokenizer):
    return [{"text": text, "chars": len(text),
             "input_tokens": len(tokenizer("passage: " + text)["input_ids"])}
            for text in pieces]


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
rec = measure_chunks(recursive, tokenizer)
print("recursive:", [(r["chars"], r["input_tokens"]) for r in rec])
print("fixed 최대 토큰:", max(r["input_tokens"] for r in measure_chunks(fixed, tokenizer)))
print("token 최대 토큰:", max(r["input_tokens"] for r in measure_chunks(token_chunks, tokenizer)))
assert [(r["chars"], r["input_tokens"]) for r in rec] == [(54, 32), (70, 40), (24, 17)], "passage: 접두사를 붙였는지 확인하세요"
assert max(r["input_tokens"] for r in measure_chunks(fixed, tokenizer)) == 45
assert max(r["input_tokens"] for r in measure_chunks(token_chunks, tokenizer)) == 51
assert set(rec[0]) == {"text", "chars", "input_tokens"}
print("\n✅ 정답이에요!")
print("생각해 보기:", "고정 분할은 최대 토큰이 더 작지만 '서면 승인' 조건을 끊었어요. 길이만으로 청크 품질을 판단할 수 없는 이유를 설명해 보세요.")
