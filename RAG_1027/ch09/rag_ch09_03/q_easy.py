# -*- coding: utf-8 -*-
# 9장 3강 퀴즈: 팀장으로 연결된 규정의 승인 조건 비교하기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 graph를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 팀장으로 들어오는 간선을 따라 어떤 규정이 팀장 승인을 요구하는지 찾아요.
# 같은 승인자라도 시점이 다르므로 조건과 원문 ID를 함께 출력해요.
policies = sorted(graph.predecessors("팀장"))
for did in policies:
    edge = graph[did]["팀장"]
    print(did, edge["condition"], edge["source_document_id"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
assert policies == ["education", "leave"], "팀장 승인은 education과 leave 두 규정이에요"
assert graph["education"]["팀장"]["condition"] == "수강 전"
assert graph["leave"]["팀장"]["condition"] == "휴가 시작 3영업일 전"
print("successors('팀장') =", list(graph.successors("팀장")), "← 방향이 반대라 비어 있어요")
print("\n✅ 정답이에요!")
print("생각해 보기:", "관계 목록에 (\"meal\", \"팀장\", \"승인자\", ...)를 원문 근거 없이 추가하면 어떤 오답이 생길지 설명해 보세요.")
