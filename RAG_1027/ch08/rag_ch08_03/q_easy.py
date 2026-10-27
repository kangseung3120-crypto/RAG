# -*- coding: utf-8 -*-
# 8장 3강 퀴즈: 금액은 같고 단위가 바뀐 답변 D 검토하기 (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 answer_review_08.json, hits를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 금액은 같지만 단위가 1박당 → 1일당으로 바뀐 답변 D를 추가하고 주장별 라벨을 직접 달아요.
# 이 비율은 수동 라벨 계산이며 RAGAS 점수가 아니에요.
answers = json.loads(Path("answer_review_08.json").read_text(
    encoding="utf-8"))["answers"]
answers["D"] = "숙박비는 1일당 12만원까지이며 숙박 영수증을 첨부해야 합니다."
d_labels = [False, True]
print(sum(d_labels) / len(d_labels))


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
travel_text = next(r["text"] for r in hits if r["document_id"] == "travel")
print("원문:", travel_text[:52])
assert "1박당 12만원" in travel_text and "1일당" not in travel_text
assert d_labels == [False, True], "금액·단위 주장은 False(1일당 ≠ 1박당), 증빙 주장은 True예요"
print("A~D 수동 비율:", {"A": 1.0, "B": 0.5, "C": 1.0, "D": sum(d_labels) / len(d_labels)})
print("\n✅ 정답이에요!")
print("생각해 보기:", "A~D 각각의 사실 오류와 질문 적합성을 표로 적고, C의 높은 근거 일치 비율을 좋은 답변으로 볼 수 없는 이유를 설명해 보세요.")
