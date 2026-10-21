"""이 강의에 포함된 청크만 읽어 임베딩 파일을 직접 만들어요."""
import json
from pathlib import Path
import numpy as np
from embedding_io import load_chunks, load_model, fingerprint, MODEL_ID

# 이 강의 ZIP에 있는 청크로 벡터를 새로 만드는 준비 단계예요.
# 다른 강의에서 생성한 파일을 복사하지 않아도 독립적으로 실행할 수 있어요.
chunks = load_chunks()
model = load_model()
# 문서 접두사를 붙인 최종 문자열의 토큰 수를 검사해요.
# 모델 한도를 넘으면 자동 절단에 맡기지 않고 청킹을 수정하도록 중단해요.
texts = ["passage: " + row["text"] for row in chunks]
lengths = [len(model.tokenizer(text, truncation=False)["input_ids"]) for text in texts]
if max(lengths, default=0) > model.max_seq_length:
    raise ValueError("모델 입력 한도를 넘는 청크가 있어요. 청킹을 다시 확인하세요.")
# 모든 문서를 같은 모델과 정규화 설정으로 변환하고 입력 순서대로 저장해요.
# 설정 파일의 지문을 통해 이후 실습에서 청크와 벡터가 맞는지 확인해요.
vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
np.save("vectors.npy", vectors)
config = {"model_id": MODEL_ID, "dimension": int(vectors.shape[1]),
          "normalized": True, "input_format": "passage: +text",
          "chunk_fingerprint": fingerprint(chunks)}
Path("embedding_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
print("준비 완료:", len(chunks), "청크", vectors.shape, "최대 입력", max(lengths), "토큰")
