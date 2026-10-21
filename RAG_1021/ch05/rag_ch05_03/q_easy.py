# -*- coding: utf-8 -*-
# 5장 3강 퀴즈: 두 검색 범위 직접 만들기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요. (먼저 uv run prepare.py)
# main.py를 먼저 실행해 current_condition, models를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 준비: main.py 끝에서 index를 닫았으므로 저장된 색인을 다시 열어요.
index = open_saved_index()

# 현재 상태 조건을 유지하고 반복문에서 범주만 바꿔 보세요.
# 필드 경로와 범주 값을 알맞게 채운 뒤 scroll로 대상 문서가 달라지는지 확인해요.
results = {}
for category in ["출장", "교육"]:
    selected = models.Filter(must=[
        current_condition,
        models.FieldCondition(
            key="metadata.category",
            match=models.MatchValue(value=category),
        ),
    ])
    records, _ = index.client.scroll(
        index.collection, scroll_filter=selected, limit=100)
    results[category] = sorted({p.payload["document_id"] for p in records})
    print(category, results[category])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert results["출장"] == ["meal", "travel"], "출장 범위에는 meal과 travel이 있어요 (travel-old는 retired)"
assert results["교육"] == ["education"]
edu = index.search("직무 교육비 지원 한도", k=5, category="출장")
print("교육비 질문을 출장으로 제한:", sorted({r["document_id"] for r in edu}))
assert "education" not in {r["document_id"] for r in edu}, "출장 필터는 정답 education을 검색 전에 제외해요"
index.close()
print("\n✅ 정답이에요!")
print("생각해 보기:", "must에서 current_condition을 빼면 어떤 문서가 더 포함될 수 있는지 자료를 읽고 답해 보세요.")
