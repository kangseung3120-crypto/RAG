"""6장 2강: 검색→Context→응답. --generate를 줄 때만 실제 Ollama 호출."""
import argparse
import json
from langchain_core.runnables import RunnableLambda
from saved_index import open_saved_index
from rag_steps import prepare, make_messages, response_schema, invoke_model, finish

# --generate를 주지 않으면 실제 검색과 예시 응답 검사까지만 실행해요.
# 모델 호출을 선택 단계로 나누어 검색 문제와 생성 문제를 구분해 볼 수 있어요.
parser = argparse.ArgumentParser()
parser.add_argument("--generate", action="store_true")
args = parser.parse_args()
index = open_saved_index()

# %% 1. 실제 검색과 Context
# prepare가 반환한 state에는 질문, 검색 청크, Context, 출처 목록이 있어요.
# 같은 상태를 뒤 단계로 넘겨 중간 결과를 추적해요.
state = prepare(index, {"question": "출장 숙박 비용 한도와 필요한 증빙은?", "k": 3})
print("[1]", [(s["id"], s["document_id"]) for s in state["sources"]])
print("Context 문자 수", len(state["context"]))
print(state["context"])

# %% 2. 모델에 보내는 두 메시지
# messages는 모델 입력이고 response_schema는 기대하는 출력 구조예요.
# 둘을 구분해서 확인하면 프롬프트 문제와 응답 형식 문제를 따로 살필 수 있어요.
messages = make_messages(state)
print("[2] roles", [m["role"] for m in messages])
print("응답 필드", response_schema()["required"])

# %% 3. 수업용으로 작성한 응답 예시로 형식과 출처 연결 확인
# 아래 답변 문장은 수업용으로 직접 작성한 예시예요.
# 검색 결과의 실제 출처 ID를 붙여 finish의 구조 검사를 연습하며 LLM 실측 결과로 해석하지 않아요.
travel_source = next(s["id"] for s in state["sources"] if s["document_id"] == "travel")
example = {"status": "answered", "answer":
    "국내 출장 숙박비는 1박당 12만원까지이며 정산할 때 숙박 영수증이 필요합니다.",
    "citations": [travel_source]}
checked = finish({**state, "draft": example})
print("[3] 응답 예시 (LLM 실측 아님)", json.dumps({k:v for k,v in checked.items() if k != "trace"}, ensure_ascii=False))

# %% 4. 보류 사유가 최종 응답에도 남는지 확인
# 보류 응답의 구체적인 사유가 후처리 뒤에도 유지되는지 확인해요.
# 없는 출처 S99를 넣은 사례는 검증 함수가 거부해야 해요.
reason = "현재 자료에는 국내 출장 규정만 있어 해외 항공 좌석 등급을 확인할 수 없습니다."
foreign = prepare(index, {"question": "해외 출장 항공 좌석 등급은?", "k": 3})
held = finish({**foreign, "draft": {"status": "insufficient", "answer": reason, "citations": []}})
print("[4] 보류 설명 보존", held["answer"] == reason, held["answer"])
try:
    finish({**state, "draft": {**example, "citations": ["S99"]}})
except ValueError as error:
    print("잘못된 출처", str(error))

# %% 5. 실제 생성은 동일한 단계를 연결해 실행
# |는 앞 함수의 반환값을 다음 함수의 입력으로 전달하는 연결이에요.
# prepare → invoke_model → finish 순서를 직접 호출할 때와 동일하게 유지해요.
chain = (RunnableLambda(lambda request: prepare(index, request))
         | RunnableLambda(invoke_model) | RunnableLambda(finish))
if args.generate:
    result = chain.invoke({"question": state["question"], "k": 3})
    print("[5] 실제 Ollama", json.dumps(result, ensure_ascii=False, indent=2))
else:
    print("[5] Ollama 미실행. --generate는 설치된 모델과 실행 중인 서버가 필요합니다.")
# TODO: 본문의 실습 코드를 이 줄 아래, 연결 종료 코드 위에 작성하세요.
index.close()
