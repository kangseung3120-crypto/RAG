"""Use the allowed evaluation model and local E5; execution must be explicit."""
import argparse
import asyncio
import json
import os
from pathlib import Path

os.environ['RAGAS_DO_NOT_TRACK'] = 'true'
import httpx
import numpy as np
from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import Faithfulness, AnswerRelevancy, ContextRecall, ContextPrecision
from local_e5 import LocalE5

# 기본 실행은 로컬 임베딩과 평가 객체 구성만 검사해요.
# --execute는 실제 유료 평가 요청, --show-recorded는 저장된 과거 검수 결과 조회예요.
parser = argparse.ArgumentParser()
parser.add_argument('--execute', action='store_true')
parser.add_argument('--show-recorded', action='store_true')
parser.add_argument('--model', choices=['gpt-6-luna', 'gpt-5.6-luna'], default='gpt-6-luna')
parser.add_argument('--max-requests', type=int, default=20)
args = parser.parse_args()
# 기록 조회는 현재 모델을 다시 실행한 결과가 아니에요.
# 예전 점수와 현재 실행 결과를 혼동하지 않도록 날짜와 실행 방식을 함께 출력해요.
if args.show_recorded:
    path = Path(__file__).resolve().parent/'recorded_results/ragas_20261007.json'
    saved = json.loads(path.read_text(encoding='utf-8'))
    print('2026-10-07 검수 기록이에요. 현재 수강생 실행 결과는 아니에요.')
    print(json.dumps({'model':saved['evaluation_model'],'embedding_model':saved['embedding_model'],
                      'scores':saved['scores'],'generation_requests':saved['generation_requests']},
                     ensure_ascii=False,indent=2))
    raise SystemExit(0)
if not 1 <= args.max_requests <= 20:
    parser.error('--max-requests must be between 1 and 20 for this small evaluation.')

# main.py가 저장한 질문 한 개와 답변 세 개를 평가 입력으로 사용해요.
# report에 모델, 호출 수, 사용량, 완료 여부를 남겨 부분 실패도 추적해요.
sample = json.loads(Path('answer_review_08.json').read_text(encoding='utf-8'))
report = {'evaluation_model': args.model, 'embedding_model': LocalE5.model_id,
          'embedding_prefix': 'query: on both questions', 'embedding_location': 'local CPU',
          'external_embedding_requests': 0, 'max_generation_requests': args.max_requests,
          'generation_requests': 0, 'api_usage': [], 'scores': {}, 'completed': False}

# 실제 전송 직전에 실행 옵션, 요청 주소, 모델명, 요청 크기와 호출 수를 검사해요.
# 이 실습은 코드에 지정된 Chat Completions 주소만 허용하므로 다른 프록시 주소는 그대로 사용할 수 없어요.
async def before_request(request):
    if not args.execute:
        raise RuntimeError('API execution is disabled in preparation mode.')
    body = await request.aread()
    payload = json.loads(body)
    if request.url.host != 'api.openai.com' or request.url.path != '/v1/chat/completions':
        raise RuntimeError('This evaluator permits only the configured chat endpoint.')
    if payload.get('model') != args.model:
        raise RuntimeError('Unexpected model; request stopped.')
    if len(body) > 40000 or payload.get('max_completion_tokens', 0) > 2048:
        raise RuntimeError('Request exceeds this evaluation input or output limit.')
    # 한 지표가 여러 LLM 요청을 만들 수 있어 답변 세 개가 요청 세 번을 뜻하지는 않아요.
    # 전송 요청 수가 설정한 한도에 도달하면 추가 요청을 중단해요.
    if report['generation_requests'] >= args.max_requests:
        raise RuntimeError('Evaluation request limit reached.')
    report['generation_requests'] += 1

# 응답에서는 상태 코드와 사용량만 기록해요.
# 키나 서비스 오류 본문을 결과 파일에 남기지 않도록 전체 응답을 그대로 저장하지 않아요.
async def after_response(response):
    await response.aread()
    entry = {'http_status': response.status_code}
    try:
        data = response.json()
        entry['usage'] = data.get('usage')
    except ValueError:
        pass
    report['api_usage'].append(entry)

# 같은 질문 두 개의 벡터가 384차원, 단위 길이, 같은 값인지 먼저 확인해요.
# 이 검사는 로컬 임베딩 연결 검증이며 RAGAS 점수 계산은 아직 수행하지 않아요.
async def main():
    embeddings = LocalE5()
    test_vectors = np.array(embeddings.embed_texts([sample['question'], sample['question']]))
    assert test_vectors.shape == (2, 384)
    assert np.allclose(np.linalg.norm(test_vectors, axis=1), 1.0, atol=1e-5)
    assert np.allclose(test_vectors[0], test_vectors[1], atol=1e-5)
    report['local_embedding_check'] = {'shape': list(test_vectors.shape), 'unit_norm': True}
    # 생성 판단에는 허용된 LLM을, 질문 유사도에는 로컬 E5를 연결해요.
    # AnswerRelevancy의 strictness=3은 답변으로부터 질문을 생성해 비교하는 평가 설정이에요.
    async with httpx.AsyncClient(event_hooks={'request': [before_request], 'response': [after_response]}) as http:
        async with AsyncOpenAI(api_key=os.environ.get('OPENAI_API_KEY') or 'preparation-only',
                               max_retries=0, timeout=60, http_client=http) as client:
            llm = llm_factory(args.model, client=client, reasoning_effort='none',
                              max_tokens=2048, max_retries=1)
            faith = Faithfulness(llm=llm)
            relevance = AnswerRelevancy(llm=llm, embeddings=embeddings, strictness=3)
            recall = ContextRecall(llm=llm)
            precision = ContextPrecision(llm=llm)
            report['metric_constructors_checked'] = True
            # 준비 모드에서는 이 지점에서 반환해 LLM 평가 호출을 생략해요.
            # 실행 모드에서는 API 키를 확인한 뒤 아래 지표 계산을 진행해요.
            if not args.execute:
                return
            if not os.environ.get('OPENAI_API_KEY'):
                raise RuntimeError('OPENAI_API_KEY is not configured.')
            # Faithfulness는 답변 주장이 근거에 의해 뒷받침되는지, AnswerRelevancy는 질문에 관련되는지를 평가해요.
            # 서로 다른 성질이라 한 점수가 높다고 다른 문제까지 해결됐다고 해석하지 않아요.
            for name, answer in sample['answers'].items():
                f = await faith.ascore(user_input=sample['question'], response=answer,
                                      retrieved_contexts=sample['retrieved_contexts'])
                r = await relevance.ascore(user_input=sample['question'], response=answer)
                report['scores'][name] = {'faithfulness': f.value, 'answer_relevancy': r.value}
                print(name, report['scores'][name], flush=True)
            # ContextRecall과 ContextPrecision에는 질문, 참고 답변, 검색 근거를 함께 전달해요.
            # 이 LLM 기반 지표는 앞 강의의 문서 ID 교집합으로 구한 Recall과 계산 방식이 달라요.
            data = {'user_input': sample['question'], 'reference': sample['reference'],
                    'retrieved_contexts': sample['retrieved_contexts']}
            report['scores']['context_recall'] = (await recall.ascore(**data)).value
            report['scores']['context_precision'] = (await precision.ascore(**data)).value
            report['completed'] = True


# 실행 도중 실패해도 finally에서 진행 기록을 저장해요.
# completed가 False인 파일의 일부 점수를 완성된 평가 결과로 해석하면 안 돼요.
try:
    asyncio.run(main())
except Exception as error:
    # Exception text may contain credentials or a service response; retain its type only.
    report['error_type'] = type(error).__name__
    raise SystemExit('Evaluation stopped: ' + type(error).__name__ + '. See the sanitized result file.')
finally:
    filename = 'ragas_local_result.json' if args.execute else 'ragas_local_preparation.json'
    Path(filename).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
