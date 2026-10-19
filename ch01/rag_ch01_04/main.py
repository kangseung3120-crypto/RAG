# -*- coding: utf-8 -*-
# 수정본 VER 2: 1장 4강 기본 예제
# rag_ch01_04 폴더에서 uv run main.py로 실행하세요.
# 접기 안의 추가 확인과 TODO 문제는 본문 안내에 따라 별도로 덧붙이세요.

import json
import hashlib
from pathlib import Path

# 현재 문서 전체를 넣는 경우와 질문 관련 문서만 넣는 경우의 입력 크기를 비교해요.
# 여기서 len은 문자 수이며 모델이 사용하는 토큰 수와는 달라요.
documents = json.loads(Path("documents.json").read_text(encoding="utf-8"))
current = [d for d in documents if d["metadata"]["status"] == "current"]
full_context = "\n".join(
    f"[{d['document_id']}] {d['content']}" for d in current
)
chosen = [d for d in current if "숙박 비용" in d["content"]]
selected_context = "\n".join(
    f"[{d['document_id']}] {d['content']}" for d in chosen
)
print("전체 입력:", len(current), "문서,", len(full_context), "문자")
print("검색 입력:", len(chosen), "문서,", len(selected_context), "문자")

# 전체 토큰 한도에서 지시문, 대화 이력, 출력 예약량, 여유분을 먼저 빼요.
# 남은 값이 문서에 쓸 수 있는 예산이고, 이미 초과했다면 0으로 제한해요.
def document_budget(context_limit, instruction, history, output, margin):
    return max(0, context_limit - instruction - history - output - margin)

# 답변을 길게 생성하도록 예약할수록 근거 문서에 쓸 수 있는 공간은 줄어들어요.
for output in [1000, 3000]:
    available = document_budget(8192, 500, 500, output, 192)
    print("출력 예약", output, "-> 문서 예산", available, "토큰")

# 모델, 접근 범위, 문서 내용이 모두 같은지 식별하는 캐시 키 예제예요.
# 해시만 만드는 코드이므로 실제 모델의 KV 캐시를 생성하거나 재사용하지는 않아요.
def prefix_key(model, scope, text):
    value = json.dumps([model, scope, text], ensure_ascii=False)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]

# 같은 조건에서는 같은 키가 나오고 모델이나 접근 범위를 바꾸면 키가 달라져요.
# 내용이 같더라도 다른 사용 권한의 캐시를 섞으면 안 되는 이유를 살펴보세요.
first = prefix_key("class-model-v1", "current", full_context)
same = prefix_key("class-model-v1", "current", full_context)
other_scope = prefix_key("class-model-v1", "all", full_context)
other_model = prefix_key("class-model-v2", "current", full_context)
print("처음:", first)
print("같은 입력:", same)
print("범위 변경:", other_scope)
print("모델 변경:", other_model)
