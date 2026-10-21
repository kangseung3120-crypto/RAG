from saved_index import open_saved_index

# 과거 금액이 들어간 질문으로 현재/과거 규정이 함께 검색되는 상황을 만들어요.
# current_only=False는 이 문제를 관찰하기 위한 비교 설정이에요.
index = open_saved_index()
question = "출장 숙박 비용 한도는 8만원인가요?"
raw = index.search(question, k=3, current_only=False)
for row in raw:
    print(row["document_id"], row["metadata"]["status"],
          row["start"], round(row["score"], 4))

# 같은 질문에 현재 상태 필터만 추가해 결과를 비교해요.
# 질문에 오래된 금액이 포함돼 있어도 현재 적용되는 규정으로 판단해야 해요.
current = index.search(question, k=3, current_only=True)
for row in current:
    print(row["document_id"], row["metadata"]["status"],
          row["start"], round(row["score"], 4))

from qdrant_client import models

# 필터의 key는 payload에 저장한 중첩 경로와 일치해야 해요.
# status가 아닌 metadata.status인 이유는 원래 자료 구조가 metadata 안에 있기 때문이에요.
current_condition = models.FieldCondition(
    key="metadata.status",
    match=models.MatchValue(value="current"),
)
current_filter = models.Filter(must=[current_condition])

# 현재 상태와 출장 범주를 must에 함께 넣어 AND 조건을 만들어요.
# 전체 Point 수와 이 조건에 맞는 Point 수를 비교해 검색 범위를 확인해요.
must = [
    models.FieldCondition(
        key="metadata.status",
        match=models.MatchValue(value="current"),
    ),
    models.FieldCondition(
        key="metadata.category",
        match=models.MatchValue(value="출장"),
    ),
]
query_filter = models.Filter(must=must)
print(index.client.count(index.collection).count)
print(index.client.count(index.collection,
      count_filter=query_filter).count)

rows = index.search(question, k=5, category="출장")
print(sorted({r["document_id"] for r in rows}))

# start >= 60 조건을 추가해 원문 앞부분을 제외한 청크를 조회해요.
# scroll은 조건에 맞는 레코드를 나열하는 기능이며 유사도 순위 검색은 아니에요.
after_first = models.Filter(
    must=must + [
        models.FieldCondition(
            key="start",
            range=models.Range(gte=60),
        )
    ]
)
# 한 번에 최대 100개를 읽어요. 더 큰 자료라면 next_offset으로 다음 페이지도 읽어야 해요.
records, next_offset = index.client.scroll(
    index.collection, scroll_filter=after_first, limit=100)
print(sorted((p.payload["document_id"], p.payload["start"])
             for p in records))

# 존재하지 않는 범주로 검색하면 빈 목록이 나와요.
# 범위 밖 자료를 억지로 반환하지 않고 이 결과를 보류나 재질문 흐름에 연결해야 해요.
missing = index.search(question, k=3, category="해외항공")
print(missing)

# 범주만 바꿔 필터 결과를 비교해요.
# set은 같은 문서의 여러 청크를 하나의 원문 ID로 모아 범위를 읽기 쉽게 해요.
for category in ["출장", "교육"]:
    selected = models.Filter(must=[current_condition, models.FieldCondition(key="metadata.category", match=models.MatchValue(value=category))])
    records, _ = index.client.scroll(index.collection, scroll_filter=selected, limit=100)
    print("실습", category, sorted({p.payload["document_id"] for p in records}))


index.close()
