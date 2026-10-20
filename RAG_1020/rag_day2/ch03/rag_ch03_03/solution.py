# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *

# 청크 본문 앞에 원문 ID와 제목을 붙여 출처와 주제를 함께 보여 줘요.
# 검색용 문자열을 보강해도 원래 page_content와 metadata는 수정하지 않아요.
def tagged_text(piece):
    title = piece.metadata["title"]
    did = piece.metadata["document_id"]
    return f"[{did}] {title}\n{piece.page_content}"

print(tagged_text(pieces[-1]))
