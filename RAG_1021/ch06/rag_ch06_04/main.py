"""6장 4강: 보류 사례를 실제 근거로 검토. --generate는 Ollama를 호출합니다."""
import argparse
import json
import httpx
from saved_index import open_saved_index
from rag_steps import prepare, invoke_model, finish

parser = argparse.ArgumentParser()
parser.add_argument("--generate", action="store_true")
args = parser.parse_args()
index = open_saved_index()
compound = "출장 식비와 숙박비의 한도는 각각 얼마이고 두 한도를 합쳐 쓸 수 있나요?"
# 근거 충분, 일부 부족, 범위 밖, 규정 미정, 질문 모호 사례를 나눠요.
# 검색 결과가 존재한다는 사실만으로 이 사례들을 같은 answered 상태로 처리하면 안 돼요.
cases = [
    ("한도와 증빙", "출장 숙박 비용 한도와 필요한 증빙은?", 3),
    ("일부 근거", compound, 1),
    ("두 문서 확보", compound, 3),
    ("범위 밖", "해외 출장 항공 좌석 등급은?", 3),
    ("규정 미정", "개인 취미 강좌도 지원하나요?", 3),
    ("대상 모호", "지원 한도는 얼마인가요?", 3),
]

# %% 1. 결과가 존재하는 것과 답할 자료가 있는 것 구분
# 먼저 각 질문의 근거만 수집해요.
# 이 단계에서 금액과 조건을 확인하면 뒤의 잘못된 답변이 검색 때문인지 생성 때문인지 구분할 수 있어요.
states = []
for label, question, k in cases:
    state = prepare(index, {"question": question, "k": k})
    states.append(state)
    print("[1]", label, "k", k, [s["document_id"] for s in state["sources"]])

# %% 2. 수업용으로 작성한 보류 응답 예시를 처리
# 보류 응답도 사용자가 다음에 무엇을 확인해야 하는지 설명해야 해요.
# 예시 응답의 사유는 남기고 citations와 최종 sources는 비어 있는지 확인해요.
example = {"status": "insufficient", "answer":
    "현재 검색 결과에는 두 한도의 합산 금지 내용만 있습니다. 식비와 숙박비 금액을 추가로 확인해야 합니다.",
    "citations": []}
checked = finish({**states[1], "draft": example})
print("[2]", checked["status"], checked["answer"])
print("보류 출처", checked["sources"])

# %% 3. 빈 Context는 모델을 호출하지 않고 처리
# 검색 근거가 전혀 없을 때는 모델을 호출하지 않는 경로를 확인해요.
# 불필요한 생성을 줄이고 근거 없는 추측을 답으로 내보내지 않게 해요.
empty = {"question": "해외 출장 항공 좌석 등급은?", "rows": [], "context": "", "sources": []}
print("[3]", finish(invoke_model(empty))["status"])

# %% 4. 수업 서버에서 실제 생성 결과 수집
# --generate일 때만 사례별 실제 모델 응답을 받아요.
# 연결/HTTP 문제는 system_error, 형식 검사 실패는 invalid_output으로 구분해요.
# 둘 다 문서에 답이 없어 정상적으로 보류한 insufficient와는 다른 상태예요.
if args.generate:
    for state in states:
        try:
            result = finish(invoke_model(state))
        except httpx.HTTPError as error:
            result = {"status": "system_error", "error_type": type(error).__name__}
        except ValueError as error:
            result = {"status": "invalid_output", "reason": str(error)}
        print("[4]", state["question"], json.dumps(result, ensure_ascii=False))
else:
    print("[4] 생성 모델 미실행. [2]는 응답 형식 연습용 예시입니다.")
# TODO: 본문의 실습 코드를 이 줄 아래, 연결 종료 코드 위에 작성하세요.
index.close()
