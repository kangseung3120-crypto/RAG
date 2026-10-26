# 기본 예제를 먼저 실행해 같은 입력과 변수를 준비한 뒤 아래 추가 실습을 실행해요.
# 이 import는 main.py의 출력과 파일 생성도 수행하므로 기본 출력이 먼저 나오는 것이 정상이에요.
from main import *
# 정답을 담은 출장 후보를 제거한 뒤 남은 후보만 다시 점수화해요.
# 재정렬기는 후보의 순서를 바꾸므로 후보에 없는 문서를 새로 검색해 주지는 않아요.
if not args.skip_model:
    reduced = [row for row in candidates if row["document_id"] != "travel"]
    new_pairs = [(run["question"], row["text"]) for row in reduced]
    new_values = model.predict(new_pairs, batch_size=4, show_progress_bar=False)
    print("후보 제거 실습:", [row["document_id"] for row in reduced], len(new_values))
