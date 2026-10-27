"""선택 실행: 같은 질문과 모델로 짧은 추출문과 Parent를 비교해요."""
# main의 검색과 부모 확장을 먼저 실행해 같은 근거를 준비해요.
# 이 파일은 짧은 근거와 부모 전체로 각각 실제 Ollama 응답을 생성하는 선택 실습이에요.
from main import *
# 추출 문장 중 앞의 두 문장만 남겨 길이는 줄지만 예외 조건이 빠질 수 있는 입력을 만들어요.
# extracted_spans에 원문 위치를 남겨 무엇을 버렸는지 확인할 수 있게 해요.
short_text = " ".join(text for start, end, text in selected[:2])
short_row = {**child, "chunk_id": child["document_id"]+":extract:first-two",
             "text": short_text, "extracted_spans": [(s,e) for s,e,t in selected[:2]]}
target = "13만원짜리 숙박도 정산할 수 있나요?"
parent_rows = [row for row in expanded if row["document_id"] == child["document_id"]]
# 질문과 생성 모델은 고정하고 Context만 바꿔 두 번 호출해요.
# 13만원 숙박의 승인 예외가 답변에 반영되는지 원문과 비교하세요.
for name, context_rows in [("짧은 추출문", [short_row]), ("Parent 전체", parent_rows)]:
    context, sources = build_context(context_rows)
    print(name, "Context:", context)
    print(json.dumps(generate_ollama(target, context, sources), ensure_ascii=False))
