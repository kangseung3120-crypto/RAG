# -*- coding: utf-8 -*-
# 1장 2강 퀴즈: 모든 검색어가 있는 문서만 찾기 (AND 검색) (정답: 교안 정답 코드예요)
# 이 폴더에서 uv run q_solution.py로 실행해요.
# main.py를 먼저 실행해 index, search_words를 준비해요. 그래서 기본 예제 출력이 먼저 나오는 게 정상이에요.

from main import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

def search_all_words(query, index):
    # Indexing 때와 같은 토큰화 규칙을 사용하고 검색 단어가 없으면 빈 결과로 끝내요.
    words = re.findall(r"[가-힣a-zA-Z0-9]+", query)
    if not words:
        return []
    # 첫 단어의 문서 집합을 복사한 뒤 나머지 단어와 교집합을 구해요.
    # 복사 없이 원래 set을 수정하면 저장된 색인이 달라질 수 있어요.
    found = set(index.get(words[0], set()))
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
