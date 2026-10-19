import os
from pathlib import Path
from rag_core import (
    read_documents, chunk_documents, retrieve, build_context, generate_ollama
)

# 기본 실습과 같은 문서, 청킹 조건, BM25 검색을 사용해 생성 단계만 추가해요.
# main.py의 검색 결과를 먼저 확인한 뒤 이 파일을 실행하면 원인을 나눠 살필 수 있어요.
documents = read_documents(Path("documents.json"))
chunks = chunk_documents(documents, size=80, overlap=20)
question = "출장 숙박 비용 한도는?"
rows = retrieve(question, chunks, method="bm25", k=3)
context, sources = build_context(rows, max_chars=260)

# 여기서 실제 Ollama 서버를 호출해요. 실행 중인 서버와 OLLAMA_MODEL 설정이 필요해요.
# 반환값은 답변 가능 여부, 답변 문장, 사용한 출처 ID로 나눠서 읽어요.
os.environ.setdefault("OLLAMA_MODEL", "gemma3:4b")
try:
    response = generate_ollama(question, context, sources)
    print(response["status"])
    print(response["answer"])
    print(response["citations"])
# ValueError는 모델 설정이나 응답 형식 검사의 실패를 보여 줘요.
# 서버 접속 오류까지 모두 처리하는 예외 구문은 아니에요.
except ValueError as error:
    print("설정 또는 응답 검사 실패:", error)

