# %% fixed
import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag_core import chunk_documents

# 같은 원문과 80자/20자 조건으로 시작해 분할 방식만 비교해요.
# fixed는 문자 위치대로 자르므로 문장 중간에서 끊길 수 있어요.
documents = [json.loads(line) for line in Path("documents.jsonl").read_text(encoding="utf-8").splitlines()]
travel = next(d for d in documents if d["document_id"] == "travel")
fixed = [c["text"] for c in chunk_documents([travel], size=80, overlap=20)]
for n, text in enumerate(fixed, 1):
    print("fixed", n, repr(text))

# %% recursive
# 마침표 뒤 공백, 공백, 마지막으로 문자 경계 순서로 분할을 시도해요.
# keep_separator=end는 구분자를 앞 조각 끝에 남기며, 겹침은 항상 정확히 20자가 되지는 않아요.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=80, chunk_overlap=20,
    separators=[". ", " ", ""], keep_separator="end",
    strip_whitespace=False,
)
recursive = splitter.split_text(travel["content"])
for n, text in enumerate(recursive, 1):
    print("recursive", n, repr(text))

# %% tokenizer
import os
from transformers import AutoTokenizer

# 임베딩에 사용할 E5와 같은 토크나이저로 길이를 재요.
# 모델 파일은 첫 실행에 내려받고 이후 캐시를 재사용할 수 있어요.
cache = os.environ.get("RAG_MODEL_CACHE", "model_cache")
tokenizer = AutoTokenizer.from_pretrained("intfloat/multilingual-e5-small",
                                        cache_dir=cache)
# passage 접두사와 특수 토큰까지 포함한 실제 입력 길이를 확인해요.
# 한글은 문자 수와 토큰 수가 다르므로 문자 기준 청크 크기만으로 입력 한도를 보장할 수 없어요.
for text in recursive:
    ids = tokenizer("passage: " + text, truncation=False)["input_ids"]
    print(ids)
    print("문자", len(text), "최종 E5 토큰", len(ids), "|", text)

# %% token_split
# 길이 함수를 E5 토크나이저로 바꿔 토큰 수를 기준으로 분할해요.
# 분할 후 접두사를 추가한 최종 입력도 다시 재서 모델 한도 안인지 확인해요.
token_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer, chunk_size=50, chunk_overlap=10,
    separators=[". ", " ", ""], keep_separator="end",
    strip_whitespace=False,
)
token_chunks = token_splitter.split_text(travel["content"])
for n, text in enumerate(token_chunks, 1):
    total = len(tokenizer("passage: " + text)["input_ids"])
    print(n, "최종 E5 토큰", total, "|", text)

# %% truncation
# 30토큰 제한으로 강제 절단한 입력과 원문을 비교하는 실패 예제예요.
# 임베딩 입력이 조용히 잘리면 뒤쪽 조건은 검색 벡터에 반영되지 않아요.
full_input = "passage: " + travel["content"]
complete = tokenizer(full_input, truncation=False)["input_ids"]
clipped = tokenizer(full_input, max_length=30, truncation=True)["input_ids"]
print("전체 입력 토큰:", len(complete), "강제로 자른 토큰:", len(clipped))
print("자른 입력을 다시 읽기:")
print(tokenizer.decode(clipped, skip_special_tokens=True))
print("원문에서 뒤에 있던 조건:")
print(travel["content"].split(". ")[2])
