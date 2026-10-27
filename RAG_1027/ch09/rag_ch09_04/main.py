"""9-4: 같은 규정으로 시각 문서 입력을 만들고 MaxSim·표 계산."""
import json
import math
import re
from pathlib import Path

# 텍스트에서 처음 등장한 만원 금액을 뽑아 원 단위 숫자로 바꿔요.
# 이 단순 정규식은 예제 문서에 맞춘 것이므로 금액이 여러 개인 실제 문서에는 단위와 대상 검사가 더 필요해요.
docs = json.loads(Path("documents.json").read_text(encoding="utf-8"))
by_id = {d["document_id"]: d for d in docs}
rows = []
for did in ["travel", "education"]:
    match = re.search(r"(\d+)만원", by_id[did]["content"])
    rows.append({"document_id": did, "title": by_id[did]["metadata"]["title"],
                 "limit_won": int(match.group(1))*10000,
                 "source_url": by_id[did]["metadata"]["source_url"]})
print("STEP1", rows)
# 숙박 문서의 1박 한도를 2박으로 곱하는 계산이에요.
# 숫자를 추출해 계산해도 승인 예외 같은 원문 조건은 별도로 확인해야 해요.
print("STEP2 숙박2박한도", rows[0]["limit_won"] * 2)
# 아래는 MaxSim의 계산 원리를 보기 위한 2차원 가상 벡터예요.
# 실제 ColPali 모델의 토큰/이미지 벡터나 추론 결과가 아니에요.
queries = [[1., 0.], [0., 1.]]
pages = {"A": [[1., 0.], [0., 1.]], "B": [[1/math.sqrt(2), 1/math.sqrt(2)]]}
# 질문 벡터 하나마다 가장 내적이 큰 페이지 벡터를 고르고 그 최대값들을 합해요.
# 페이지 전체를 평균 벡터 하나로 줄이는 방식과 다른 다중 벡터 비교예요.
def maxsim(query_vectors, page_vectors):
    return sum(max(sum(a*b for a, b in zip(q, p)) for p in page_vectors) for q in query_vectors)
print("STEP3 MaxSim 수치모형", {k: round(maxsim(queries, v), 4) for k, v in pages.items()})
print("MODEL_NOT_RUN: 위 2차원 벡터는 계산용 입력이며 ColPali 출력이 아닙니다.")
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("PAGES_NOT_CREATED: uv add pillow==12.3.0 후 다시 실행하세요.")
else:
    # 같은 규정을 이미지 페이지로 그려 선택 실습의 실제 입력 파일을 만들어요.
    # Windows 한글 글꼴이 필요하며 이 단계는 OCR이나 이미지 검색 모델 추론이 아니에요.
    out = Path("visual_pages")
    out.mkdir(exist_ok=True)
    font_path = Path("C:/Windows/Fonts/malgun.ttf")
    if not font_path.exists():
        raise RuntimeError("한글 글꼴 경로를 수업 환경의 글꼴로 지정하세요.")
    title_font = ImageFont.truetype(str(font_path), 48)
    text_font = ImageFont.truetype(str(font_path), 30)
    import textwrap
    # 문서별 이미지를 따로 저장하고 원문 ID와 페이지 번호를 그림에 표시해 출처를 남겨요.
    # 줄바꿈 폭과 이미지 높이는 이 짧은 예제 문서에 맞춘 값이에요.
    for did in ["travel", "education"]:
        doc = by_id[did]
        image = Image.new("RGB", (1200, 900), "#ffffff")
        draw = ImageDraw.Draw(image)
        draw.rectangle((50, 50, 1150, 160), fill="#e8efff")
        draw.text((80, 80), doc["metadata"]["title"], font=title_font, fill="#163a72")
        y = 215
        for line in textwrap.wrap(doc["content"], width=30):
            draw.text((80, y), line, font=text_font, fill="#15223b")
            y += 60
        draw.text((80, 810), f"원문 ID: {did} / page 1", font=text_font, fill="#566477")
        image.save(out / f"{did}.png")
    print("STEP4", sorted(p.name for p in out.glob("*.png")))
