"""Display the instructor's prior run without model calls."""
import json
from pathlib import Path

# 함께 제공한 이전 검수의 개수와 세 질의 응답을 읽는 조회 전용 코드예요.
# 모델을 호출하지 않으므로 현재 환경에서 같은 결과를 재현했다는 검증으로 사용할 수 없어요.
folder=Path(__file__).resolve().parent/'recorded_results'
print('2026-10-07 검수 기록이에요. 현재 수강생 실행 결과는 아니에요.')
index=json.loads((folder/'index_20261007.json').read_text(encoding='utf-8'))
print(json.dumps(index['counts'],ensure_ascii=False,indent=2))
# Local, Global, DRIFT는 서로 다른 검색 범위를 사용해요.
# 저장된 질문과 답변을 함께 읽고 원문의 핵심 조건이 유지됐는지 비교하세요.
for method in ['local','global','drift']:
    result=json.loads((folder/f'{method}_20261007.json').read_text(encoding='utf-8'))
    print('\n'+method.upper(),result['question'])
    print(result['response'])
print('\n모델 응답은 실행마다 달라질 수 있어요. 세 질문의 주요 규정만 대조한 기록이에요.')
