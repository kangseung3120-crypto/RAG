"""Optional OpenAI-compatible embedding comparison; no request without --execute."""
import argparse
import json
import os
from pathlib import Path
import time
import numpy as np
from rag_core import evaluate

# 기본 실행은 입력 건수와 예상 요청 수만 출력해요.
# 실제 외부 임베딩 요청은 --execute와 사용 가능한 임베딩 모델명을 지정했을 때만 진행해요.
parser = argparse.ArgumentParser()
parser.add_argument('--execute',action='store_true')
parser.add_argument('--model',default=os.environ.get('EMBEDDING_API_MODEL',''))
args = parser.parse_args()
# E5 비교와 같은 청크와 dev 질문을 사용해 입력 자료 차이의 영향을 줄여요.
# 외부 모델에는 E5 전용 접두사를 붙이지 않고 그 모델에 맞는 입력을 사용해요.
chunks = json.loads(Path('chunks.json').read_text(encoding='utf-8'))
golden = [json.loads(line) for line in Path('golden.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
dev = [row for row in golden if row['split']=='dev']
plan = {'documents':len(chunks),'questions':len(dev),'maximum_requests':2,
        'input_format':'plain text; no E5-specific prefixes',
        'model':args.model or '미설정','executed':False}
if not args.execute:
    print(json.dumps(plan,ensure_ascii=False,indent=2))
    raise SystemExit(0)
if not args.model or not os.environ.get('OPENAI_API_KEY'):
    parser.error('OPENAI_API_KEY와 사용 권한이 있는 --model 값을 준비하세요.')
if len(chunks)>40 or len(dev)>20:
    parser.error('이 비교는 청크 40개와 질문 20개 이하의 소규모 입력만 허용해요.')
from openai import OpenAI

# API 응답의 index로 원래 입력 순서를 복원하고 누락/중복을 검사해요.
# 각 벡터를 정규화해 아래 내적 검색에서 코사인 유사도를 사용할 수 있게 해요.
def vectors_from(response,count):
    rows=sorted(response.data,key=lambda row:row.index)
    if [row.index for row in rows] != list(range(count)):
        raise ValueError('임베딩 응답의 행 번호나 개수가 입력과 달라요.')
    vectors=np.asarray([row.embedding for row in rows],dtype=np.float64)
    lengths=np.linalg.norm(vectors,axis=1,keepdims=True)
    if vectors.ndim!=2 or not np.isfinite(vectors).all() or np.any(lengths==0):
        raise ValueError('유효한 임베딩 벡터를 받지 못했어요.')
    return vectors/lengths

# 문서 묶음과 질문 묶음에 각각 한 번씩 요청해요. max_retries=0으로 자동 재시도 호출을 막아요.
# LLM 대화 모델 사용 권한과 임베딩 모델 사용 권한은 별도일 수 있어요.
try:
    with OpenAI(max_retries=0,timeout=60) as client:
        started=time.perf_counter()
        doc_response=client.embeddings.create(model=args.model,input=[c['text'] for c in chunks])
        documents=vectors_from(doc_response,len(chunks))
        document_seconds=time.perf_counter()-started
        started=time.perf_counter()
        question_response=client.embeddings.create(model=args.model,input=[q['question'] for q in dev])
        questions=vectors_from(question_response,len(dev))
        if documents.shape[1]!=questions.shape[1]:
            raise ValueError('문서와 질문의 임베딩 차원이 달라요.')
        # 질문 벡터를 미리 저장해 평가 중 추가 API 호출이 생기지 않게 해요.
        # 검색은 현재 문서에 대해 정확한 내적 계산을 하고 상위 세 청크를 반환해요.
        query_by_text={row['question']:vector for row,vector in zip(dev,questions)}
        def search(question,category=None):
            scores=documents @ query_by_text[question]
            eligible=[i for i,c in enumerate(chunks) if c['metadata']['status']=='current']
            order=sorted(eligible,key=lambda i:(-float(scores[i]),chunks[i]['chunk_id']))
            return [{**chunks[i],'score':float(scores[i])} for i in order[:3]]
        # 질문별 결과와 사용량을 파일로 남겨 로컬 E5 결과와 비교해요.
        # API의 일괄 요청 시간과 E5의 순차 질문 시간은 측정 방식이 달라 그대로 속도 우열을 판단할 수 없어요.
        report=evaluate(dev,search)
        result={**plan,'executed':True,'dimension':int(documents.shape[1]),'k':3,'report':report,
                'document_seconds':document_seconds,'query_batch_and_search_seconds':time.perf_counter()-started,
                'timing_comparable_to_sequential_e5':False,
                'usage':[doc_response.usage.model_dump(),question_response.usage.model_dump()]}
        Path('api_embedding_comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False,indent=2))
except Exception as error:
    # Do not print a provider error body or an API key.
    raise SystemExit('API 비교 중단: '+type(error).__name__+'. 키 권한, 모델명, 입력 제한을 확인하세요.')
