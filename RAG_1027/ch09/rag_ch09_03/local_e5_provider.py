"""Native GraphRAG provider backed by actual CPU E5 embeddings, without an API."""
import asyncio
from functools import lru_cache
from threading import RLock
import numpy as np
from sentence_transformers import SentenceTransformer
from graphrag_llm.embedding.embedding import LLMEmbedding
from graphrag_llm.types import LLMEmbedding as EmbeddingRow, LLMEmbeddingResponse, LLMEmbeddingUsage

_lock = RLock()


# 같은 모델을 호출할 때마다 다시 로딩하지 않도록 한 모델을 캐시해요.
# 모델 추론 구간은 아래 잠금으로 보호해 동시에 공유 모델을 사용하지 않게 해요.
@lru_cache(maxsize=1)
def load_model(name):
    return SentenceTransformer(name, device='cpu')


class LocalE5Embedding(LLMEmbedding):
    # GraphRAG 설정에서 모델명과 E5 접두사를 받아요.
    # 문서/보고서는 passage, 질의는 query로 설정하며 벡터 차원은 같은 모델을 기준으로 맞춰요.
    def __init__(self, *, model_config, tokenizer, metrics_store, **kwargs):
        self.name = model_config.model
        self.prefix = (model_config.model_extra or {}).get('e5_prefix', 'passage: ')
        self._tokenizer = tokenizer
        self._metrics_store = metrics_store
        self.model = load_model(self.name)
        self.long_inputs_split = 0

    # 문자열 하나와 문자열 목록을 모두 목록 형태로 맞추고 잘못된 입력을 거부해요.
    # 응답 index를 유지해 GraphRAG가 입력과 벡터를 같은 순서로 연결할 수 있게 해요.
    def embedding(self, /, **kwargs):
        texts = kwargs['input']
        if isinstance(texts, str):
            texts = [texts]
        if not texts or not all(isinstance(text, str) for text in texts):
            raise ValueError('Local E5 expects one or more text strings.')
        rows = []
        with _lock:
            for index, text in enumerate(texts):
                # 원문 토큰을 최대 480개씩 나눠 E5 입력 한도 안에서 처리해요.
                # 디코딩 후 접두사와 특수 토큰이 다시 붙으므로 최종 토큰 길이도 재검사해요.
                ids = self.model.tokenizer(text, add_special_tokens=False, verbose=False)['input_ids']
                # Preserve long GraphRAG reports instead of silently truncating them.
                windows = [ids[start:start+480] for start in range(0, len(ids), 480)] or [[]]
                if len(windows) > 1:
                    self.long_inputs_split += 1
                parts = [self.prefix + self.model.tokenizer.decode(part, skip_special_tokens=True)
                         for part in windows]
                encoded_lengths = [len(self.model.tokenizer(part, verbose=False)['input_ids'])
                                   for part in parts]
                if max(encoded_lengths) > self.model.max_seq_length:
                    raise ValueError('E5 segment exceeds its input limit after decoding; reduce the window size.')
                # 각 창을 정규화된 벡터로 만든 뒤 창의 토큰 수를 가중치로 평균을 내요.
                # 긴 문서를 한 벡터로 압축하는 방법이라 세부 조건의 검색 민감도는 별도로 평가해야 해요.
                vectors = self.model.encode(parts, batch_size=4, normalize_embeddings=True,
                                            show_progress_bar=False)
                weights = np.array([max(1, len(part)) for part in windows])
                vector = np.average(vectors, axis=0, weights=weights)
                # 평균 벡터는 더 이상 길이 1이 아닐 수 있어 다시 정규화해요.
                # 0벡터는 나눗셈이 불가능하므로 오류로 처리해요.
                norm = np.linalg.norm(vector)
                if not norm:
                    raise ValueError('E5 returned a zero vector.')
                rows.append(EmbeddingRow(object='embedding', embedding=(vector/norm).tolist(), index=index))
        # GraphRAG가 기대하는 응답 구조로 벡터를 감싸요.
        # usage의 0은 외부 API 과금 기록이 없다는 뜻이며 로컬에서 토큰을 전혀 처리하지 않았다는 뜻은 아니에요.
        return LLMEmbeddingResponse(object='list', data=rows, model=self.name,
                                    usage=LLMEmbeddingUsage(prompt_tokens=0, total_tokens=0))

    # 동기 CPU 추론을 작업 스레드에서 실행해 비동기 호출 인터페이스와 연결해요.
    # 내부 잠금 때문에 이 구현이 여러 추론을 동시에 처리한다는 의미는 아니에요.
    async def embedding_async(self, /, **kwargs):
        return await asyncio.to_thread(self.embedding, **kwargs)

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def metrics_store(self):
        return self._metrics_store


# 설정 파일의 provider 이름 local_e5를 이 클래스에 등록해요.
# GraphRAG CLI를 호출하기 전에 같은 프로세스 안에서 한 번 실행해야 해요.
def register():
    from graphrag_llm.embedding import register_embedding
    register_embedding('local_e5', LocalE5Embedding, scope='singleton')
