"""선택 실습: Ollama로 q10 검색 표현 생성. 실제 모델 연결이 필요합니다."""
import json
import os
from pathlib import Path
import httpx
# 질문의 의도를 유지하는 검색 표현을 최대 두 개 추가하는 선택 실습이에요.
# 응답에 정답 금액이나 문서의 사실을 추측해서 끼워 넣지 않도록 지시해요.
golden = [json.loads(s) for s in Path("golden.jsonl").read_text(encoding="utf-8").splitlines()]
question = next(g["question"] for g in golden if g["question_id"] == "q10")
schema = {"type": "object", "properties": {"queries": {"type": "array", "items": {"type": "string"}, "maxItems": 2}}, "required": ["queries"], "additionalProperties": False}
messages = [{"role": "system", "content": "같은 정보 요구를 나타내는 검색 문장 2개를 JSON queries로 반환하세요. 원질문에 없는 답, 금액, 문서의 사실을 추가하지 마세요. 관련 대화: 수강을 완료한 뒤 교육비 정산에 필요한 서류를 묻고 있습니다."}, {"role": "user", "content": question}]
# 여기서 실제 Ollama 서버를 호출해요. OLLAMA_MODEL은 설치된 모델 태그여야 해요.
# 원질문과 재작성 결과를 함께 기록해 의도가 바뀌지 않았는지 읽어 보세요.
url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/") + "/api/chat"
with httpx.Client(timeout=120) as client:
    response = client.post(url, json={"model": os.environ["OLLAMA_MODEL"], "messages": messages, "format": schema, "stream": False})
    response.raise_for_status()
    model_text = response.json()["message"]["content"]
# 응답을 JSON으로 해석하지 못하면 빈 객체로 두어 원질문만 사용해요.
# 그다음 루트 객체, queries 목록, 각 문자열을 순서대로 검사해요.
try:
    value = json.loads(model_text)
except (json.JSONDecodeError, TypeError):
    value = {}
# 잘못된 JSON/루트 타입/queries 타입이면 원질문만 유지합니다.
generated = value.get("queries", []) if isinstance(value, dict) else []
if not isinstance(generated, list):
    generated = []
# 원질문은 항상 보존하고 비어 있지 않은 새 표현만 최대 두 개 추가해요.
# 같은 검색문이 반복돼 호출 수만 늘어나는 일을 막기 위해 중복을 제거해요.
texts = [question]
for item in generated[:2]:
    if isinstance(item, str):
        clean = item.strip()
        if clean and clean not in texts:
            texts.append(clean)
print(json.dumps(texts, ensure_ascii=False, indent=2))


from rag_core import bm25
chunks = json.loads(Path("chunks.json").read_text(encoding="utf-8"))
current = [c for c in chunks if c["metadata"]["status"] == "current"]
# 생성한 표현별 실제 검색 결과를 비교해 원래 의도의 근거를 더 찾았는지 판단해요.
# 형식 검사는 통과했어도 재작성 문장의 의미가 맞는지는 별도로 확인해야 해요.
for query in texts:
    rows = bm25(query, current, k=3)
    print(query, [(r["document_id"], r["start"]) for r in rows])
