from saved_index import open_saved_index

# 식비와 숙박비를 함께 묻는 질문으로 여러 근거를 모아요.
# 검색된 각 청크에서 금액, 단위, 합산 가능 여부 중 어떤 조건을 확인할 수 있는지 읽어 보세요.
index = open_saved_index()
question = "출장 식비와 숙박비의 한도는 각각 얼마이고 두 한도를 합쳐 쓸 수 있나요?"
rows = index.search(question, k=3)
for rank, row in enumerate(rows, 1):
    print(rank, row["document_id"], row["start"], len(row["text"]))
    print(row["text"])

# 첫 청크를 일부러 중복으로 넣고 chunk_id를 키로 사용해 중복을 제거해요.
# 같은 원문의 서로 다른 청크는 내용이 다를 수 있으므로 document_id만으로 제거하지 않아요.
repeated = rows + [rows[0]]
unique = list({row["chunk_id"]: row for row in repeated}.values())
print("입력", len(repeated), "중복 제거", len(unique))
print([(r["document_id"], r["start"]) for r in unique])

# 모델에 넣는 문자열은 본문 외에도 출처 라벨과 제목을 포함해요.
# 이 부가 정보의 길이까지 계산해야 실제 입력 예산을 넘기지 않아요.
first = unique[0]
label = "S1"
piece = f'[{label}] {first["metadata"]["title"]}\n{first["text"]}'
print(piece)
print("본문", len(first["text"]), "라벨·제목 포함", len(piece))

# 검색 순서대로 근거를 넣되 전체 길이가 max_chars 안에 들어가는 조각만 선택해요.
# 이 함수의 예산은 토큰 수가 아닌 문자 수이고, sources에는 실제 포함한 근거만 기록해요.
def pack_context(rows, max_chars):
    pieces, sources = [], []
    used = 0
    for row in rows:
        label = f"S{len(sources) + 1}"
        piece = f'[{label}] {row["metadata"]["title"]}\n{row["text"]}'
        # 구분용 줄바꿈 두 문자까지 예약해 보수적으로 길이를 계산해요.
        # 큰 조각이 들어가지 않으면 건너뛰고 다음 조각을 확인해요.
        if used + len(piece) + 2 > max_chars:
            continue
        pieces.append(piece)
        # S1 같은 라벨을 청크 ID, 원문 ID, URL과 연결해 답변에서 출처를 복원할 수 있게 해요.
        sources.append({
            "id": label, "chunk_id": row["chunk_id"],
            "document_id": row["document_id"],
            "source_url": row["metadata"]["source_url"],
        })
        used += len(piece) + 2
    return "\n\n".join(pieces), sources

# 같은 검색 결과라도 예산을 줄이면 필요한 규정이 Context에서 빠질 수 있어요.
# 검색 단계의 성공과 생성 단계에 필요한 근거 확보를 구분해서 확인하세요.
for budget in [120, 200, 300]:
    context, sources = pack_context(unique, max_chars=budget)
    print(budget, "실제 길이", len(context),
          [(s["id"], s["document_id"]) for s in sources])

context, sources = pack_context(unique, max_chars=300)
print(context)
print(sources[2]["id"], sources[2]["source_url"])

# 검색 k와 Context 예산을 함께 바꾸며 실제 들어간 원문 ID와 본문을 대조해요.
# k만 늘려도 예산이 부족하면 추가 근거를 모델에 전달하지 못할 수 있어요.
for k, budget in [(1, 300), (3, 200), (3, 300)]:
    found = index.search(question, k=k)
    packed, source_map = pack_context(found, max_chars=budget)
    print("실습 k", k, "예산", budget, [s["document_id"] for s in source_map])
    print(packed)


index.close()
