# %% inspect
import json
from pathlib import Path

# JSONL 한 줄을 문서 하나로 복원하고 출장 본문의 문자 위치를 살펴봐요.
# text[:80]과 text[80:160]은 토큰이 아닌 Python 문자열의 문자 구간이에요.
documents = [json.loads(line) for line in Path("documents.jsonl").read_text(encoding="utf-8").splitlines()]
travel = next(d for d in documents if d["document_id"] == "travel")
text = travel["content"]
print("원문 문자 수:", len(text))
print("첫 80자:", text[:80])
print("다음 80자:", text[80:160])

# %% window
# size는 한 청크의 최대 문자 수이고 overlap은 다음 청크와 겹칠 문자 수예요.
# 이 기본 함수는 유효한 인수를 전제로 하므로 0 <= overlap < size를 지켜야 해요.
def windows(text, size, overlap):
    result = []
    # 이동 간격은 size - overlap이에요. 80자와 겹침 20자라면 시작점이 0, 60, 120으로 이동해요.
    for start in range(0, len(text), size - overlap):
        # 마지막 구간이 원문 길이를 넘지 않게 end를 제한해요.
        # 반환값은 시작 위치, 끝 위치, 실제 본문이며 끝 위치는 슬라이스에 포함되지 않아요.
        end = min(start + size, len(text))
        result.append((start, end, text[start:end]))
        if end == len(text):
            break
    return result

for start, end, piece in windows(text, 80, 20):
    print(f"[{start}:{end}]", piece)

# %% compare
# 청크 수와 저장 문자 수를 함께 비교해요.
# 겹침은 경계의 맥락을 보존하지만 중복 저장량도 늘리므로 비용과 함께 판단해요.
for size, overlap in [(80, 0), (80, 20), (100, 20)]:
    pieces = windows(text, size, overlap)
    print(size, overlap, "청크", len(pieces), "저장 문자", sum(len(p[2]) for p in pieces))
print("겹치는 구간 [60:80]:", text[60:80])
