# -*- coding: utf-8 -*-
# 1장 2강 퀴즈: 모든 검색어가 있는 문서만 찾기 (AND 검색) (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q_easy.py로 실행해요.
# main.py를 먼저 실행해 index, search_words를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 모든 질문 단어가 들어 있는 문서만 남기는 AND 검색을 완성해요.
# 빈칸(____)을 채우세요. 각 TODO 바로 아래 코드가 그 TODO의 답이에요.
def search_all_words(query, index):
    words = re.findall(r"[가-힣a-zA-Z0-9]+", query)
    # TODO 1: 검색어가 없으면 빈 목록을 반환하세요.
    if not words:
        return []
    # TODO 2: 첫 단어가 포함된 문서 집합에서 시작하세요.
    found = set(index.get(words[0], set()))
    # TODO 3: 다음 단어마다 공통 문서 ID만 남기세요.
    for word in words[1:]:
        found.intersection_update(index.get(word, set()))
    return sorted(found)


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
saved = {w: set(v) for w, v in index.items()}
for query in ["숙박 교육비는", "숙박 영수증을"]:
    print(query)
    print("OR:", search_words(query, index))
    print("AND:", search_all_words(query, index))

assert search_all_words("숙박 교육비는", index) == []
assert search_all_words("숙박 영수증을", index) == ["travel"]
assert search_all_words("   ", index) == []
assert index == saved, "검색하면서 색인(index)이 바뀌었어요. 첫 집합을 set()으로 복사했는지 확인하세요."
print("\n✅ 정답이에요!")
print("생각해 보기:", "OR 검색과 AND 검색의 결과 차이를 합집합과 교집합으로 설명해 보세요.")
