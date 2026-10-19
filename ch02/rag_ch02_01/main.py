# %% text
import json
from pathlib import Path

# 같은 출장 규정을 TXT, HTML, PDF에서 읽어 결과를 비교해요.
# documents.json의 travel은 비교 기준이며 raw 폴더의 파일들이 실제 로더 입력이에요.
documents = json.loads(Path("documents.json").read_text(encoding="utf-8"))
travel = next(d for d in documents if d["document_id"] == "travel")
raw_text = Path("raw/travel.txt").read_text(encoding="utf-8")
print(raw_text)

# %% html
from html.parser import HTMLParser

# HTMLParser가 태그를 만나면 아래 메서드를 호출해요.
# in_p가 True인 동안만 텍스트를 모아 메뉴나 제목 태그의 내용을 제외해요.
# 단순한 p 태그 예제용 파서라 복잡한 웹 문서에는 별도의 본문 추출 규칙이 필요해요.
class ParagraphParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag == "p": self.in_p = True
    def handle_endtag(self, tag):
        if tag == "p": self.in_p = False
    def handle_data(self, data):
        if self.in_p: self.parts.append(data)

# feed가 HTML을 순서대로 읽으며 parts를 채워요.
# 모은 문단을 공백으로 연결한 결과가 검색에 사용할 html_text예요.
parser = ParagraphParser()
parser.feed(Path("raw/travel.html").read_text(encoding="utf-8"))
html_text = " ".join(parser.parts).strip()
print(html_text)

# %% pdf
from pypdf import PdfReader

# PDF 첫 페이지의 텍스트 계층을 추출해요. 페이지 번호는 0부터 시작해요.
# 이 코드는 OCR이 아니므로 스캔 이미지 PDF는 같은 방법으로 본문이 나오지 않을 수 있어요.
reader = PdfReader("raw/travel.pdf")
page_text = reader.pages[0].extract_text()
print("페이지 수:", len(reader.pages))
print(page_text)

# %% document
from langchain_core.documents import Document

# Document의 page_content에는 검색할 본문을, metadata에는 출처 정보를 담아요.
# 기존 메타데이터를 펼친 뒤 원문 ID와 입력 형식을 추가해 로더가 달라도 같은 구조로 다뤄요.
loaded = Document(page_content=html_text, metadata={**travel["metadata"],
                  "document_id": travel["document_id"], "format": "html"})
print(loaded.metadata["document_id"], loaded.metadata["title"])
print(loaded.page_content[:60])
