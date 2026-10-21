# %% sections
import json
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# 교육비와 재택근무 문서를 제목이 있는 Markdown으로 구성해요.
# 제목을 경계로 나누면 서로 다른 규정이 한 청크에 섞이는 일을 줄일 수 있어요.
documents = [json.loads(line) for line in Path("documents.jsonl").read_text(encoding="utf-8").splitlines()]
chosen = [d for d in documents if d["document_id"] in {"education", "remote"}]
markdown = "\n\n".join(f"## {d['metadata']['title']}\n{d['content']}" for d in chosen)
print(markdown)

# %% header
# ## 제목을 section 메타데이터로 남기는 1차 분할이에요.
# 원문 제목으로 원래 문서를 찾아 출처와 document_id를 다시 연결해요.
header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##", "section")])
sections = header_splitter.split_text(markdown)
by_title = {d["metadata"]["title"]: d for d in chosen}
for section in sections:
    original = by_title[section.metadata["section"]]
    section.metadata.update(original["metadata"])
    section.metadata["document_id"] = original["document_id"]
    print(section.metadata["document_id"], section.metadata["section"])
    print(section.page_content[:60])

# %% size
# 먼저 나눈 절 안에서만 길이 기준의 2차 분할을 해요.
# split_documents는 본문을 나누면서 해당 절의 메타데이터도 전달해요.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=80, chunk_overlap=20, separators=[". ", " ", ""],
    keep_separator="end", strip_whitespace=False,
)
pieces = splitter.split_documents(sections)
for piece in pieces:
    print(piece.metadata["document_id"], "|", piece.page_content)

# %% title_text
# 본문만으로 주제를 알기 어려운 청크에는 제목을 함께 임베딩하는 방식을 비교할 수 있어요.
# 여기서는 입력 문자열만 만들며 실제 벡터를 생성하지는 않아요.
piece = pieces[0]
embedding_text = piece.metadata["title"] + "\n" + piece.page_content
print("검색용 입력:")
print(embedding_text)
education = next(d for d in chosen if d["document_id"] == "education")
print("마지막 조건:", education["content"].split(". ")[-1])
