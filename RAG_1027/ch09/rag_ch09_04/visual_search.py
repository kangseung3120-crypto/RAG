"""ColPali 선택 실습: main.py가 만든 실제 페이지 이미지를 검색."""
from pathlib import Path
import torch
from PIL import Image
from colpali_engine.models import ColPali, ColPaliProcessor

# 이 파일은 실제 ColPali 가중치를 내려받아 추론하는 선택 실습이에요.
# GPU가 없으면 CPU를 선택하지만 큰 모델이라 충분한 메모리와 실행 시간이 필요해요.
name = "vidore/colpali-v1.3"
device = "cuda" if torch.cuda.is_available() else "cpu"
# GPU 경로는 bfloat16을 사용하므로 장치의 해당 자료형 지원도 확인해야 해요.
# eval은 학습용 동작을 평가 모드로 바꾸며 아래 no_grad는 기울기 저장을 생략해요.
dtype = torch.bfloat16 if device == "cuda" else torch.float32
model = ColPali.from_pretrained(name, torch_dtype=dtype, device_map=device).eval()
processor = ColPaliProcessor.from_pretrained(name)
# main.py가 만든 두 페이지 이미지를 RGB로 읽고 질문을 별도 입력으로 준비해요.
# 이미지 순서를 유지해야 점수 열과 실제 파일 경로를 올바르게 연결할 수 있어요.
paths = [Path("visual_pages/travel.png"), Path("visual_pages/education.png")]
images = [Image.open(p).convert("RGB") for p in paths]
queries = ["출장 숙박비 한도와 필요한 증빙은 무엇인가요?"]
# processor가 이미지와 질문을 모델이 받는 텐서로 변환해요.
# 입력과 모델을 같은 장치에 놓은 뒤 이미지/질문의 다중 벡터를 각각 추론해요.
batch_images = processor.process_images(images).to(model.device)
batch_queries = processor.process_queries(queries).to(model.device)
with torch.no_grad():
    image_vectors = model(**batch_images)
    query_vectors = model(**batch_queries)
# score_multi_vector는 질문별로 각 페이지와의 다중 벡터 유사도를 계산해요.
# 첫 행은 첫 질문, 각 열은 paths의 페이지에 대응하며 가장 큰 점수의 페이지를 선택해요.
scores = processor.score_multi_vector(query_vectors, image_vectors)
print("점수 행렬:", scores)
best = int(scores[0].argmax())
print("선택 페이지:", paths[best])
# 선택된 페이지의 원문 ID와 페이지 번호를 남겨요.
# 이 코드는 페이지 검색까지 수행하며 질문에 대한 문장 답변을 생성하거나 사실성을 판정하지는 않아요.
print("원문 ID:", paths[best].stem, "표시 페이지: 1")

