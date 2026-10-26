# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# 먼저 여섯 후보를 합친 뒤 서로 다른 원문에서 한 청크씩 선택해 문서 다양성을 확보해요.
# 다만 같은 원문의 추가 청크에 필요한 조건이 있다면 이 방식이 오히려 근거를 줄일 수 있어요.
fused = reciprocal_rank_fusion(rankings, k=6)
selected, seen_documents = [], set()
for row in fused:
    did = row["document_id"]
    if did not in seen_documents:
        selected.append(row)
        seen_documents.add(did)
    if len(selected) == 2: break
print("문서 다양성 실습:", [(r["document_id"], r["start"]) for r in selected])
