from saved_index import open_saved_index
from rag_steps import prepare

# 검색에서 얻은 sources 라벨을 실제 청크 본문에 다시 연결할 준비를 해요.
index = open_saved_index()
state = prepare(index, {
    "question": "출장 숙박 비용 한도와 필요한 증빙은?",
    "k": 3,
})
print([(s["id"], s["document_id"]) for s in state["sources"]])

# 먼저 chunk_id로 청크를 찾는 표를 만들고, S1 같은 출처 ID를 해당 청크에 연결해요.
# 라벨은 이번 응답 안에서만 유효하므로 다른 질문의 S1과 같은 출처라고 가정하면 안 돼요.
by_chunk = {r["chunk_id"]: r for r in state["rows"]}
lookup = {
    source["id"]: by_chunk[source["chunk_id"]]
    for source in state["sources"]
}
print(lookup["S1"]["text"])
print(lookup["S1"]["metadata"]["source_url"])

# claim.text는 답변의 주장이고 claim.quote는 근거에서 가져온 인용문이에요.
# 처음에는 둘을 같은 문장으로 만들어 원문 일치 검사를 확인해요.
quote = "국내 출장 숙박 비용 한도는 1박당 12만원입니다."
claim = {
    "source_id": "S1",
    "text": quote,
    "quote": quote,
}
print(claim["quote"] in lookup["S1"]["text"])

from urllib.parse import urlparse

# 출처 존재 여부, 인용문 포함 여부, URL 형식을 차례로 확인해 실패 원인을 구분해요.
# URL 형식 검사는 실제 페이지 접속이나 공개 열람을 확인하는 검사는 아니에요.
def bind_claim(claim, lookup):
    source = lookup.get(claim["source_id"])
    if source is None:
        return "unknown_source", None
    if claim["quote"] not in source["text"] or not claim["quote"].strip():
        return "quote_not_found", None
    url = source["metadata"]["source_url"]
    if urlparse(url).scheme not in {"http", "https"} or not urlparse(url).netloc:
        return "invalid_url", None
    # 주장과 인용문이 다르면 뜻이 같은지 추가 검토가 필요해요.
    # 원문에 인용문이 있다는 사실만으로 답변의 단위나 조건까지 올바르다고 볼 수 없어요.
    status = "extractive_match" if claim["text"] == claim["quote"] else "review_meaning"
    return status, {"text": claim["text"], "url": url, "quote": claim["quote"]}

status, linked = bind_claim(claim, lookup)
print(status)
print(linked["text"])
print(linked["url"])

# 없는 출처, 원문에 없는 금액, 1박 한도를 전체 일정 한도로 바꾼 사례를 비교해요.
# 각 실패가 어느 검사에서 발견되고 어느 부분은 의미 검토로 남는지 확인해요.
variants = [
    {**claim, "source_id": "S99"},
    {**claim, "quote": "숙박비는 20만원입니다."},
    {**claim, "text": "출장 전체의 숙박비는 최대 12만원입니다."},
]
for candidate in variants:
    print(bind_claim(candidate, lookup)[0])

# 같은 출처에서도 금액 외에 영수증 조건을 별도 주장으로 연결해요.
# 답변의 핵심 조건마다 근거가 있는지 확인하는 연습이에요.
receipt = "숙박 영수증을 첨부해야 정산할 수 있습니다."
receipt_claim = {
    "source_id": "S1",
    "text": receipt,
    "quote": receipt,
}
status2, linked2 = bind_claim(receipt_claim, lookup)
print(status2)
print(linked2["text"])

# TODO: 본문의 실습 코드를 이 줄 아래, 연결 종료 코드 위에 작성하세요.

index.close()
