# -*- coding: utf-8 -*-
# 3장 3강 퀴즈: 청크의 원문을 알아볼 수 있게 출력하기 (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 pieces를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 청크 본문 앞에 원문 ID와 제목을 붙여 출처와 주제를 함께 보여 줘요.
# 검색용 문자열을 보강해도 원래 page_content와 metadata는 수정하지 않아요.
def tagged_text(piece):
    title = piece.metadata["title"]
    did = piece.metadata["document_id"]
    return f"[{did}] {title}\n{piece.page_content}"


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
before = (pieces[-1].page_content, dict(pieces[-1].metadata))
out = tagged_text(pieces[-1])
print(out)
assert out.splitlines()[0] == "[remote] 재택근무 운영"
assert "오전 10시부터 오후 4시까지" in out and "근무 장소 변경" in out
assert (pieces[-1].page_content, dict(pieces[-1].metadata)) == before, "metadata와 본문을 바꾸지 마세요"
assert tagged_text(pieces[0]).startswith("[education] 교육비 지원\n")
print("\n✅ 정답이에요!")
print("생각해 보기:", "크기를 80→60으로 줄이면 각 ID의 청크 수가 어떻게 바뀌고, 교육비 마지막 조건이 온전히 읽히는지 확인해 보세요.")
