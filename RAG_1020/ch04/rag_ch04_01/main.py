"""4장 1강 순차 실행 예제. 이 강의 폴더에서 uv run으로 실행해요."""
import json
from pathlib import Path
import numpy as np
from embedding_io import load_chunks, load_model, fingerprint, MODEL_ID

# %% 1. 앞 장의 청크 읽기
# ZIP에 포함된 chunks.json을 읽으므로 앞 강의 폴더를 가져올 필요는 없어요.
# 문서 수와 청크 수가 다른 이유를 출장 문서의 시작/끝 위치로 확인해요.
chunks = load_chunks()
print("[1] 문서/청크", len({c["document_id"] for c in chunks}), len(chunks))
print("travel offsets", [(c["start"], c["end"]) for c in chunks if c["document_id"] == "travel"])

# %% 2. 패딩을 제외한 평균과 정규화: 계산용 값
# 계산 원리를 보여 주기 위한 3개 토큰의 2차원 가상 벡터예요.
# 마지막 행은 패딩으로 보고 mask=0을 주어 평균에서 제외해요. 실제 E5 출력값은 아니에요.
tokens = np.array([[1., 2.], [3., 0.], [99., 99.]])
mask = np.array([1., 1., 0.])
# mask[:, None]은 마스크를 열 방향으로 늘려 각 토큰 벡터의 모든 성분에 적용해요.
# 유효 토큰 수로 나눈 뒤 L2 길이로 다시 나누면 길이 1의 벡터가 돼요.
pooled = (tokens * mask[:, None]).sum(axis=0) / mask.sum()
unit = pooled / np.linalg.norm(pooled)
print("[2] 평균", pooled.tolist(), "정규화", unit.round(4).tolist())
print("패딩 포함 평균", tokens.mean(axis=0).round(2).tolist())

# %% 3. 실제 E5 임베딩
# 여기부터 실제 E5 small을 사용해 청크마다 임베딩을 만들어요.
# passage 접두사를 포함한 토큰 길이를 출력하고 모델 한도와 비교하세요.
model = load_model()
passages = ["passage: " + c["text"] for c in chunks]
lengths = [len(model.tokenizer(p)["input_ids"]) for p in passages]
# 입력 순서대로 벡터가 반환되므로 vectors[i]와 chunks[i]가 한 쌍이에요.
# normalize_embeddings=True를 사용해 뒤 실습에서 내적으로 코사인 유사도를 계산할 수 있어요.
vectors = model.encode(passages, normalize_embeddings=True, show_progress_bar=False)
print("[3] shape", vectors.shape, "최대 입력 토큰", max(lengths))
print("norm 처음 3행", np.linalg.norm(vectors[:3], axis=1).round(6).tolist())

# %% 4. 다음 장에 전달할 파일
# 벡터만 저장하면 어떤 모델과 청크로 만들었는지 알 수 없어요.
# 차원, 정규화 여부, 입력 형식, 청크 지문을 설정 파일에 함께 기록해 재사용 조건을 남겨요.
np.save("vectors.npy", vectors)
config = {"model_id": MODEL_ID, "dimension": int(vectors.shape[1]),
    "normalized": True, "input_format": "passage: +text",
    "chunk_fingerprint": fingerprint(chunks)}
Path("embedding_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
print("[4] 저장", np.load("vectors.npy").shape)
