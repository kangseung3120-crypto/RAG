# -*- coding: utf-8 -*-
# 3장 2강 퀴즈: 분할 결과를 한 표로 비교하기 (Hard: TODO를 직접 완성해요)
# 이 폴더에서 uv run q_hard.py로 실행해요.
# main.py를 먼저 실행해 fixed, recursive, token_chunks, tokenizer를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 문자 길이와 최종 E5 입력 토큰 길이를 함께 기록하는 과제예요.
# 접두사와 특수 토큰이 포함되는지 확인하고 청크마다 한 딕셔너리를 반환하세요.
def measure_chunks(pieces, tokenizer):
    rows = []
    # TODO: 본문과 len(text)를 기록하세요.
    # TODO: passage prefix를 붙인 input_ids 길이를 기록하세요.
    # TODO: 청크별 dict 목록을 반환하세요.
    raise NotImplementedError


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
