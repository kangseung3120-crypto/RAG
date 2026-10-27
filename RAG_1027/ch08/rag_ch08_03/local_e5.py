"""RAGAS question similarity with local multilingual E5 and symmetric prefixes."""
import asyncio
from ragas.embeddings.base import BaseRagasEmbedding
from sentence_transformers import SentenceTransformer


# RAGAS가 요구하는 임베딩 인터페이스에 로컬 E5를 연결하는 어댑터예요.
# 평가 LLM 호출은 별도로 필요하지만 이 클래스는 외부 임베딩 API를 호출하지 않아요.
class LocalE5(BaseRagasEmbedding):
    model_id = 'intfloat/multilingual-e5-small'

    def __init__(self):
        super().__init__()
        self.model = SentenceTransformer(self.model_id, device='cpu')

    # 단일 문자열도 묶음 처리 함수를 재사용하고 첫 번째 벡터를 꺼내요.
    # 두 경로가 같은 접두사와 정규화 설정을 사용하게 하는 구조예요.
    def embed_text(self, text, **kwargs):
        return self.embed_texts([text], **kwargs)[0]

    def embed_texts(self, texts, **kwargs):
        # AnswerRelevancy compares the original question with generated questions.
        # Both sides therefore use the symmetric query prefix, not passage.
        # AnswerRelevancy는 원질문과 답변에서 생성한 질문을 비교해요.
        # 양쪽 모두 질문이므로 query 접두사를 동일하게 붙이고 문서용 passage는 사용하지 않아요.
        inputs = ['query: ' + text for text in texts]
        # 최종 입력이 모델 한도 안인지 검사한 뒤 길이 1로 정규화된 벡터를 반환해요.
        # 목록 형태로 바꾸어 RAGAS의 임베딩 인터페이스에 맞춰요.
        lengths = [len(self.model.tokenizer(text, verbose=False)['input_ids']) for text in inputs]
        if max(lengths, default=0) > self.model.max_seq_length:
            raise ValueError('평가 질문이 E5 입력 한도를 넘었어요. 질문 길이와 입력을 확인하세요.')
        return self.model.encode(inputs,
                                 normalize_embeddings=True, show_progress_bar=False).tolist()

    # 비동기 호출 인터페이스를 제공하지만 이 구현의 CPU 추론은 내부에서 동기 실행돼요.
    # 대량 병렬 처리를 최적화한 구현으로 해석하지 않아요.
    async def aembed_text(self, text, **kwargs):
        return self.embed_text(text, **kwargs)

    async def aembed_texts(self, texts, **kwargs):
        return self.embed_texts(texts, **kwargs)
