# RAG 4일차 실습 자료 (6장 오전 · 7장 오후)

6장과 7장 강의 8개의 실습 폴더를 하나로 묶었어요. **uv 실행 환경은 이 폴더에 하나만 만들고 8개 강의가 함께 써요.** 그래서 오늘은 처음에 한 번만 세팅하면 돼요.

## 폴더 구성

```
rag_day4/
├─ pyproject.toml      ← 8개 강의에 필요한 패키지 목록 (함께 씀)
├─ uv.lock             ← 패키지 버전 고정 (함께 씀)
├─ .python-version     ← Python 3.12 (함께 씀)
├─ ch06/  (오전)
│  ├─ rag_ch06_01/     6장 1강  Retriever 결과와 Context 구성
│  ├─ rag_ch06_02/     6장 2강  기본 2-Step RAG 체인 구현
│  ├─ rag_ch06_03/     6장 3강  출처가 보이는 Citation 응답
│  └─ rag_ch06_04/     6장 4강  근거 부족 시 답변 보류
└─ ch07/  (오후)
   ├─ rag_ch07_01/     7장 1강  BM25와 Dense 검색 비교
   ├─ rag_ch07_02/     7장 2강  Hybrid Search와 RRF
   ├─ rag_ch07_03/     7장 3강  Cross-Encoder Re-ranking
   └─ rag_ch07_04/     7장 4강  Query Rewrite와 Multi-Query
```

강의 폴더 안의 파일은 노션 교안의 ZIP과 같아요. 여기에 퀴즈 파일 3개(`q_easy.py`, `q_hard.py`, `q_solution.py`)를 더했어요.

## 처음 한 번만: 세팅

1. **압축 풀기:** ZIP을 OneDrive와 동기화되지 않는 곳(예: `C:\rag`)에 풀어요. 바탕 화면이나 문서 폴더가 OneDrive와 동기화돼 있으면 설치 중에 오류가 날 수 있어요.
2. **폴더 열기:** VS Code에서 **파일 → 폴더 열기**로 `rag_day4` 폴더를 열어요. 강의 폴더가 아니라 이 루트 폴더를 열어요.
3. **터미널에서 설치:** **터미널 → 새 터미널**(PowerShell)을 열고 아래를 실행해요.

```powershell
# uv와 Python 3.12가 준비됐는지 확인해요.
uv --version
uv python install 3.12
# 8개 강의에 필요한 패키지를 한 번에 설치해요. rag_day4 폴더에서 실행해요.
uv sync
```

`.venv` 폴더가 `rag_day4` 바로 아래에 하나 생기면 끝이에요. 패키지 구성은 3일차와 같아요. PyTorch가 함께 설치돼서 몇 분 걸릴 수 있어요.

- E5 모델(`intfloat/multilingual-e5-small`)은 전에 한 번 받았다면 그대로 다시 써요.
- 7장 3강은 재정렬 모델(`cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`, 약 470MB)을 처음 실행할 때 내려받아요.

> **교안의 "실습 준비"와 다른 점:** 교안은 강의마다 `uv init`, `uv python pin`, `uv add`를 하라고 안내해요. 이 묶음에서는 위의 `uv sync` 한 번으로 대신하므로, **강의 폴더 안에서 `uv init`을 실행하지 마세요.** 실행하면 그 강의 폴더에만 환경이 따로 생겨요.

## 강의마다: 실행

강의 폴더로 이동해서 실행해요. uv가 상위 폴더의 환경을 자동으로 찾아 써요. **먼저 실행할 파일이 강의마다 달라요.**

| 강의 | 먼저 | 그다음 |
| --- | --- | --- |
| 6장 1 ~ 4강 | `uv run prepare.py` (벡터 만들기) | `uv run main.py` |
| 7장 1강 | 없음 | `uv run main.py` |
| 7장 2강 · 3강 | `uv run prepare.py` (검색 결과 파일 만들기) | `uv run main.py` |
| 7장 4강 | 없음 | `uv run main.py` |

```powershell
# 예: 6장 1강
cd ch06\rag_ch06_01
uv run prepare.py
uv run main.py
uv run solution.py

# 예: 7장 2강 (rag_day4에서 다시 이동해요)
cd ..\..\ch07\rag_ch07_02
uv run prepare.py
uv run main.py
```

- `prepare.py`는 한 번만 실행하면 돼요. 6장은 `vectors.npy`와 `embedding_config.json`을, 7장 2 · 3강은 `search_runs_07.json`을 만들어요. 빠뜨리면 `FileNotFoundError`가 나요.
- 7장 3강에서 모델을 내려받기 어렵다면 `uv run main.py --skip-model`로 후보와 입력 쌍까지만 확인해요.
- Qdrant는 `:memory:` 모드로 Python 안에서 실행돼요. 서버 설치, 계정, API 키가 필요 없어요.
- 강의 폴더마다 교안 "기본 실습" 문제가 세 가지 파일로 들어 있어요. 통과하면 `✅ 정답이에요!`가 나와요.
  - `q_easy.py`: 교안의 빈칸(`____`) 그대로
  - `q_hard.py`: 같은 문제를 TODO로 바꾼 버전
  - `q_solution.py`: 교안 정답
- 퀴즈 파일은 `main.py`를 먼저 실행한 뒤 문제를 풀어요. 그래서 기본 예제 출력이 먼저 나와요. `main.py`가 끝에서 연결을 닫으면 퀴즈 파일이 필요한 연결을 다시 열어요.
- 직접 실습 코드를 `main.py`에 쓸 때는 **`client.close()` / `index.close()` / `dense.close()` 위**에 써요.

## VS Code 편집기 설정 (import 밑줄이 보일 때)

Ctrl+Shift+P → **Python: Select Interpreter** → `rag_day4\.venv\Scripts\python.exe`를 골라요. 8개 강의 모두 이 하나로 돼요.

## 선택 실습: Ollama로 실제 답변 · 검색 표현 생성

기본 실행은 모델 없이 동작해요. 실제 모델 결과까지 보려면 Ollama가 필요해요. `httpx`는 이미 설치돼 있어서 `uv add`는 필요 없어요.

```powershell
ollama pull gemma3:4b-it-q4_K_M
$env:OLLAMA_MODEL = "gemma3:4b-it-q4_K_M"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
cd ch06\rag_ch06_02
uv run main.py --generate
cd ..\..\ch07\rag_ch07_04
uv run rewrite.py
```

- 6장 2강 · 4강 `--generate`: 실제 답변 생성
- 7장 4강 `rewrite.py`: 모델이 만든 검색 표현으로 BM25 검색

환경 변수는 현재 터미널에만 적용돼요. 새 터미널을 열었다면 다시 지정해요. 모델 응답은 환경과 버전에 따라 달라요.

## 막힐 때

| 증상 | 확인할 것 |
| --- | --- |
| `uv sync` 중 `os error 396` (하드 링크 오류) | OneDrive 동기화 폴더예요. `setx UV_LINK_MODE copy`를 실행하고 터미널을 새로 연 뒤 다시 `uv sync` 해요. 압축을 동기화되지 않는 폴더에 다시 푸는 것도 방법이에요 |
| `.venv\Lib\site-packages\transformers\...py` 파일이 없다는 `FileNotFoundError` | 압축을 푼 경로가 너무 길어요(Windows 경로 260자 제한). `C:\rag`처럼 짧은 경로에 다시 풀고 `uv sync` 해요 |
| `FileNotFoundError: embedding_config.json` | 6장 강의 폴더에서 `uv run prepare.py`를 먼저 실행해요 |
| `FileNotFoundError: search_runs_07.json` | 7장 2 · 3강 폴더에서 `uv run prepare.py`를 먼저 실행해요 |
| 7장 3강 모델 다운로드 실패 | 인터넷 연결과 저장 공간(약 470MB)을 확인하고, 안 되면 `uv run main.py --skip-model` |
| client / index / dense가 닫혔다는 오류 | 실습 코드를 `close()` 위로 옮겨요 |
| `--generate` · `rewrite.py`에서 Connection refused | Ollama 앱이 실행 중인지, `OLLAMA_BASE_URL`이 `http://localhost:11434`인지 확인해요 |
| `KeyError: 'OLLAMA_MODEL'` · model not found | `ollama list`에 나온 태그를 `OLLAMA_MODEL`에 정확히 넣어요 |
| HF 토큰 · symlink · `position_ids UNEXPECTED` 경고 | 모델을 받거나 불러올 때 나오는 안내 문구예요. 실행 결과에는 영향이 없어요 |
| `ModuleNotFoundError` | `rag_day4` 폴더에서 `uv sync`를 했는지, `uv run`으로 실행했는지 확인해요 |
| 강의 폴더에 `pyproject.toml`이 생겼어요 | 실수로 `uv init`을 실행한 거예요. 그 강의 폴더의 `pyproject.toml`, `.python-version`, `.venv`를 지우면 다시 공용 환경을 써요 |

## 검증 기록

- 2026-10-25 · Windows 11 · Python 3.12에서 확인했어요.
- 7장 강의 4개의 `prepare.py` · `main.py` · `solution.py`를 공용 환경으로 실행한 결과가 교안의 "전체 기본 실행 결과"와 같았어요 (예: 7-1 IDF(숙박) 2.8134 · q10 BM25 [] · Dense education@0 0.8398, 7-2 RRF 0.032787 · 0.032002 · 합집합 9, 7-3 쌍 토큰 55 ~ 70 · travel@0 -0.346, 7-4 합집합 3 · 검색 횟수 3).
- 6장 강의 4개는 3일차 묶음과 같은 파일이에요 (3일차에 같은 방식으로 검증).
- 퀴즈 8개 모두 `q_solution.py`가 통과하고, `q_easy.py` 빈칸을 정답으로 채우면 통과하는 것을 확인했어요.
