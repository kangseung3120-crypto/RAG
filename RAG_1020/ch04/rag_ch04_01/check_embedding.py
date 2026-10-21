"""Check the default local embedding model without a paid API call."""
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# 공개 E5 small 모델을 CPU에 불러와요. 첫 다운로드에는 인터넷이 필요해요.
# 질문에는 query, 문서에는 passage 접두사를 붙여 모델이 입력 역할을 구분하게 해요.
model_id = 'intfloat/multilingual-e5-small'
model = SentenceTransformer(model_id, device='cpu')
texts = ['query: 출장 숙박비 한도는 얼마인가요?', 'passage: 숙박비 한도는 1박당 12만원입니다.']
# 토큰 길이를 먼저 검사해 입력의 뒷부분이 자동으로 잘리는 상황을 막아요.
lengths = [len(model.tokenizer(text)['input_ids']) for text in texts]
if max(lengths) > model.max_seq_length:
    raise ValueError('입력이 모델 길이 제한을 넘었어요. 청크 길이를 줄이세요.')
# 두 입력을 길이 384의 벡터 두 행으로 바꾸고 각 행의 길이를 1로 정규화해요.
# 아래 assert는 차원과 정규화 확인이며 검색 정답 여부를 평가하는 검사는 아니에요.
vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
assert vectors.shape == (2,384)
assert np.allclose(np.linalg.norm(vectors,axis=1),1,atol=1e-5)
print(json.dumps({'model':model_id,'device':'cpu','shape':list(vectors.shape),
                  'normalized':True,'input_within_limit':True,'embedding_api_calls':0},ensure_ascii=False))
