# -*- coding: utf-8 -*-
# 7장 1강 퀴즈: BM25가 놓친 교육비 근거를 Dense 결과에서 읽기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 chunks, golden, current, bm25, DenseIndex를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 준비: main.py 끝에서 dense를 닫았으므로 새 DenseIndex를 만들어요.
dense = DenseIndex(chunks)

# q10은 BM25 결과가 비어 있었어요. 같은 질문의 Dense 상위 6개에서 교육 규정 청크만 골라 읽어요.
# 질문에 필요한 서류가 어느 위치(start)의 청크에 있는지 확인하세요.
question = next(g["question"] for g in golden if g["question_id"] == "q10")
found = []
for row in dense.search(question, k=6):
    if row["document_id"] == "education":
        found.append(row["start"])
        print(row["start"], row["text"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("BM25 결과:", bm25(question, current, k=6))
assert bm25(question, current, k=6) == [], "공백 토큰화 BM25는 q10에서 아무것도 못 찾아요"
assert sorted(found) == [0, 60], "Dense 상위 6개에는 education 청크가 두 개(start 0, 60) 있어요"
rows = {r["start"]: r["text"] for r in dense.search(question, k=6) if r["document_id"] == "education"}
assert "수료증과 영수증" in rows[60], "필요한 서류는 start 60 청크에 있어요"
assert "수료증" not in rows[0]
dense.close()
print("\n✅ 정답이에요!")
print("생각해 보기:", "Dense 1위는 education 0인데 정답 서류는 education 60에 있어요. k=1로 검색했다면 답변이 어떻게 됐을지 설명해 보세요.")
