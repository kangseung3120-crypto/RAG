"""Exercise GraphRAG's embedding factory without any generation calls."""
import asyncio
import json
import os
from pathlib import Path
import numpy as np
from graphrag.config.load_config import load_config
from graphrag_llm.embedding import create_embedding
from local_e5_provider import register

# 설정의 local_e5 이름을 실제 Python 구현에 연결하는 등록을 먼저 해요.
# 임시 키 문자열은 설정 로딩용이며 이 준비 검사에서는 생성 API를 호출하지 않아요.
register()
os.environ.setdefault('OPENAI_API_KEY','local-check-no-generation')
project_dir = Path(__file__).resolve().parent
graph_root = project_dir / 'graphrag_demo'
config = load_config(root_dir=graph_root)
# 문서용과 질문용 설정을 각각 만들어 passage/query 접두사가 구분되도록 해요.
# 공식 임베딩 팩터리를 거쳐 실제 수업 설정이 구현과 연결되는지 확인해요.
documents = create_embedding(config.embedding_models['default_embedding_model'])
queries = create_embedding(config.embedding_models['query_embedding_model'])
paths = sorted((graph_root / 'input').glob('*.txt'))
texts = [path.read_text(encoding='utf-8') for path in paths]
# 입력 문서 열 개와 질문 하나를 실제 로컬 E5로 임베딩해요.
# 차원과 정규화를 검사하고 질문과 가장 가까운 문서가 travel인지 확인해요.
doc_response = documents.embedding(input=texts)
question = '출장 숙박비 한도와 증빙은 무엇인가요?'
query_response = asyncio.run(queries.embedding_async(input=[question]))
vectors = np.array([row.embedding for row in doc_response.data])
query_vector = np.array(query_response.first_embedding)
assert vectors.shape == (10, 384)
assert query_vector.shape == (384,)
assert np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=1e-5)
ranked = np.argsort(-(vectors @ query_vector))
assert paths[int(ranked[0])].stem == 'travel'
# 긴 가상 문서를 넣어 자동 절단 대신 여러 창으로 나누는 경로도 실행해요.
# 벡터를 얻었다는 사실이 긴 문서의 세부 의미까지 완전히 보존한다는 뜻은 아니에요.
long_response = documents.embedding(input=['Long document example. ' * 700])
assert len(long_response.first_embedding) == 384
assert documents.long_inputs_split > 0
# 이 보고서는 임베딩 연결 검사 결과예요.
# GraphRAG의 엔티티 추출, 그래프 색인, 질의까지 완료했다는 기록으로 해석하지 않아요.
report = {'provider': 'local_e5', 'model': documents.name, 'document_shape': list(vectors.shape),
          'query_shape': list(query_vector.shape), 'unit_norm': True,
          'long_input_strategy': '480-token windows; length-weighted mean; normalize again',
          'long_input_test_passed': True, 'external_embedding_requests': 0,
          'query_top3_document_ids': [paths[int(i)].stem for i in ranked[:3]],
          'generation_requests': 0, 'graphrag_index_executed': False}
(project_dir / 'local_embedding_preparation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
