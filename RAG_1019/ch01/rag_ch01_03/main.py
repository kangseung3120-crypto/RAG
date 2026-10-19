# -*- coding: utf-8 -*-
# 수정본 VER 2: 1장 3강 기본 예제
# rag_ch01_03 폴더에서 uv run main.py로 실행하세요.
# 접기 안의 추가 확인과 TODO 문제는 본문 안내에 따라 별도로 덧붙이세요.

from pathlib import Path
from RAG_1019.ch01.rag_ch01_03.rag_core import read_documents, chunk_documents, retrieve, build_context

# 원문을 검수한 뒤 80자 청크를 만들고 인접 청크끼리 20자를 겹쳐요.
# 청크에는 원문 ID와 시작 위치가 남아 있어 검색 뒤에도 출처를 찾을 수 있어요.
documents = read_documents(Path("documents.json"))
chunks = chunk_documents(documents, size=80, overlap=20)
print("문서", len(documents), "청크", len(chunks))

# BM25는 질문 단어의 등장 빈도와 희소성으로 후보를 정렬해요.
# k=3은 최대 세 청크를 받는다는 뜻이며 세 문서를 보장하지는 않아요.
question = "출장 숙박 비용 한도는?"
rows = retrieve(question, chunks, method="bm25", k=3)
for rank, row in enumerate(rows, 1):
    print(rank, row["document_id"], f"{row['score']:.3f}")
    print(row["text"])

# 검색 결과 중 260자 예산에 들어가는 근거를 Context로 묶어요.
# sources는 S1 같은 표시와 원문 ID를 연결하는 출처 목록이에요.
context, sources = build_context(rows, max_chars=260)
print(context)
print("인용 연결:", [(s["id"], s["document_id"]) for s in sources])

# 같은 검색 결과라도 입력 예산이 작으면 빠지는 근거가 생겨요.
# 출처 목록과 실제 Context를 함께 보고 어느 조건이 사라졌는지 확인해요.
for budget in [110, 260]:
    small_context, small_sources = build_context(rows, max_chars=budget)
    print("예산", budget, "->",
          [(s["id"], s["document_id"]) for s in small_sources])
    print(small_context)
