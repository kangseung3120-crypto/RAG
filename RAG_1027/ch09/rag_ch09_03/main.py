"""9-3: 원문 근거가 있는 관계의 실제 NetworkX 탐색과 GraphRAG 입력 준비."""
import json
from pathlib import Path
import networkx as nx

# 현재 규정만 골라 원문 ID로 조회할 수 있게 해요.
# 아래 관계는 원문을 읽고 사람이 만든 교육용 입력이며 LLM 자동 추출 결과가 아니에요.
docs = json.loads(Path("documents.json").read_text(encoding="utf-8"))
by_id = {d["document_id"]: d for d in docs if d["metadata"]["status"] == "current"}
# 각 관계는 원문에서 직접 확인한 것입니다. 자동 추출 결과가 아닙니다.
relations = [
    ("travel", "영수증", "제출", "숙박 정산"),
    ("education", "영수증", "제출", "수강 완료 후"),
    ("education", "수료증", "제출", "수강 완료 후"),
    ("meal", "영수증", "제출", "출장 식비 정산"),
    ("travel", "담당 임원", "승인자", "한도 초과 숙박 예약 전 서면 승인"),
    ("education", "팀장", "승인자", "수강 전"),
    ("leave", "팀장", "승인자", "휴가 시작 3영업일 전"),
    ("vpn", "관리자", "승인자", "VPN 계정 발급"),
]
# 규정 → 제출물/승인자 방향의 간선을 만들고 관계, 조건, 원문 출처를 함께 저장해요.
# 같은 승인자라도 적용 시점이 다르므로 condition을 빠뜨리면 의미를 잘못 합칠 수 있어요.
graph = nx.DiGraph()
for did, entity, relation, condition in relations:
    graph.add_edge(did, entity, relation=relation, condition=condition,
                   source_document_id=did, source_url=by_id[did]["metadata"]["source_url"])
print("STEP1", graph.number_of_nodes(), graph.number_of_edges())
# 영수증으로 들어오는 간선을 따라 어떤 규정이 영수증을 요구하는지 찾고,
# 각 규정의 나가는 간선에서 승인자를 확인해 두 관계를 연결해요.
policies = sorted(graph.predecessors("영수증"))
print("STEP2 영수증 제출 규정", policies)
for did in policies:
    approvals = [(v, edge["condition"]) for _, v, edge in graph.out_edges(did, data=True)
                 if edge["relation"] == "승인자"]
    print(did, approvals if approvals else "승인자 규정 없음", by_id[did]["metadata"]["source_url"])
print("STEP3 원문확인", by_id["travel"]["content"])
# 현재 규정을 문서별 TXT로 저장해 실제 GraphRAG 입력을 준비해요.
# 이 파일 생성과 NetworkX 탐색만으로 공식 GraphRAG 색인이 수행되는 것은 아니에요.
target = Path("graphrag_demo/input")
target.mkdir(parents=True, exist_ok=True)
for did, doc in by_id.items():
    (target / f"{did}.txt").write_text(
        f"document_id: {did}\n출처: {doc['metadata']['source_url']}\n제목: {doc['metadata']['title']}\n\n{doc['content']}\n",
        encoding="utf-8")
print("STEP4 GraphRAG 입력", len(list(target.glob("*.txt"))), "개")
print("GRAPHRAG_NOT_RUN: NetworkX 탐색과 입력파일 생성은 실행; 공식 색인/LLM query는 선택 실습")
