# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *

#  질문 임베딩과 입력 잘림
# 질문도 같은 384차원 공간으로 바꾸되 문서와 다른 query 접두사를 사용해요.
query = model.encode("query: 출장 호텔비는 얼마까지인가요?", normalize_embeddings=True)
print("[5] 질문 shape", query.shape, "norm", round(float(np.linalg.norm(query)), 6))
# 청크를 반복해 긴 입력을 만들고 토큰 한도 초과 여부만 확인해요.
# 이 예제는 긴 입력을 실제로 임베딩하지 않으므로 잘린 벡터를 검색에 사용하지 않아요.
long_input = "passage: " + chunks[0]["text"] * 30
print("긴 입력 한도 초과", len(model.tokenizer(long_input, truncation=False)["input_ids"]) > model.max_seq_length)
