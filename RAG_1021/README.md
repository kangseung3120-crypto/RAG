# RAG 3일차 실습 자료 (5장 오전 · 6장 오후)

5장과 6장 강의 8개의 실습 폴더를 하나로 묶었어요. **uv 실행 환경은 이 폴더에 하나만 만들고 8개 강의가 함께 써요.** 그래서 오늘은 처음에 한 번만 세팅하면 돼요.

## 폴더 구성

```
rag_day3/
├─ pyproject.toml      ← 8개 강의에 필요한 패키지 목록 (함께 씀)
├─ uv.lock             ← 패키지 버전 고정 (함께 씀)
├─ .python-version     ← Python 3.12 (함께 씀)
├─ ch05/  (오전)
│  ├─ rag_ch05_01/     5장 1강  Vector Store와 Qdrant 데이터 모델
│  ├─ rag_ch05_02/     5장 2강  Collection 생성/Upsert/Query
│  ├─ rag_ch05_03/     5장 3강  Metadata Filter와 검색 범위 제어
│  └─ rag_ch05_04/     5장 4강  데이터 갱신과 ANN 검색 개요
└─ ch06/  (오후)
   ├─ rag_ch06_01/     6장 1강  Retriever 결과와 Context 구성
   ├─ rag_ch06_02/     6장 2강  기본 2-Step RAG 체인 구현
   ├─ rag_ch06_03/     6장 3강  출처가 보이는 Citation 응답
   └─ rag_ch06_04/     6장 4강  근거 부족 시 답변 보류
```

강의 폴더 안의 파일은 노션 교안의 ZIP과 같아요. 여기에 퀴즈 파일 3개(`q_easy.py`, `q_hard.py`, `q_solution.py`)를 더했어요.

## 처음 한 번만: 세팅

1. **압축 풀기:** ZIP을 OneDrive와 동기화되지 않는 곳(예: `C:\rag`)에 풀어요. 바탕 화면이나 문서 폴더가 OneDrive와 동기화돼 있으면 설치 중에 오류가 날 수 있어요.
2. **폴더 열기:** VS Code에서 **파일 → 폴더 열기**로 `rag_day3` 폴더를 열어요. 강의 폴더가 아니라 이 루트 폴더를 열어요.
3. **터미널에서 설치:** **터미널 → 새 터미널**(PowerShell)을 열고 아래를 실행해요.

```powershell
# uv와 Python 3.12가 준비됐는지 확인해요.
uv --version
uv python install 3.12
# 8개 강의에 필요한 패키지를 한 번에 설치해요. rag_day3 폴더에서 실행해요.
uv sync
```

`.venv` 폴더가 `rag_day3` 바로 아래에 하나 생기면 끝이에요. 2일차처럼 PyTorch가 함께 설치돼서 몇 분 걸릴 수 있어요.

E5 모델(`intfloat/multilingual-e5-small`)은 2일차에 한 번 받았다면 그대로 다시 써요. 처음이라면 첫 `prepare.py`를 실행할 때 내려받아요.

> **교안의 "실습 준비"와 다른 점:** 교안은 강의마다 `uv init`, `uv python pin`, `uv add`를 하라고 안내해요. 이 묶음에서는 위의 `uv sync` 한 번으로 대신하므로, **강의 폴더 안에서 `uv init`을 실행하지 마세요.** 실행하면 그 강의 폴더에만 환경이 따로 생겨요.

## 강의마다: 실행

강의 폴더로 이동한 뒤 **`prepare.py`를 먼저** 실행하고 `main.py`를 실행해요. uv가 상위 폴더의 환경을 자동으로 찾아 써요.

```powershell
# 예: 5장 1강
cd ch05\rag_ch05_01
uv run prepare.py
uv run main.py
uv run solution.py

# 다음 강의로 갈 때는 rag_day3에서 다시 이동해요.
cd ..\..\ch06\rag_ch06_01
uv run prepare.py
uv run main.py
```

- **8개 강의 모두 `uv run prepare.py`를 먼저 실행해요.** 그 폴더의 청크로 `vectors.npy`와 `embedding_config.json`을 만들어요. 먼저 실행하지 않으면 `FileNotFoundError: embedding_config.json`이 나요. 청크를 바꾸지 않았다면 다시 실행할 필요는 없어요.
- Qdrant는 `:memory:` 모드로 Python 안에서 실행돼요. 서버 설치, 계정, API 키가 필요 없어요.
- 강의 폴더마다 교안 "기본 실습" 문제가 세 가지 파일로 들어 있어요. 통과하면 `✅ 정답이에요!`가 나와요.
  - `q_easy.py`: 교안의 빈칸(`____`) 그대로
  - `q_hard.py`: 같은 문제를 TODO로 바꾼 버전
  - `q_solution.py`: 교안 정답
- 퀴즈 파일은 `main.py`를 먼저 실행한 뒤 문제를 풀어요. 그래서 기본 예제 출력이 먼저 나와요. `main.py`가 끝에서 연결을 닫으므로 퀴즈 파일이 필요한 연결을 다시 열어요.
- 직접 실습 코드를 `main.py`에 쓸 때는 **`client.close()` / `index.close()` 위**에 써요.

## VS Code 편집기 설정 (import 밑줄이 보일 때)

Ctrl+Shift+P → **Python: Select Interpreter** → `rag_day3\.venv\Scripts\python.exe`를 골라요. 8개 강의 모두 이 하나로 돼요.

## 선택 실습: 6장 2강 · 4강 실제 답변 생성 (Ollama)

기본 실행은 모델 없이 동작해요(사람이 쓴 응답 예시로 형식 검사). 실제 답변까지 보려면 Ollama가 필요해요. `httpx`는 이미 설치돼 있어서 `uv add`는 필요 없어요.

```powershell
ollama pull gemma3:4b-it-q4_K_M
$env:OLLAMA_MODEL = "gemma3:4b-it-q4_K_M"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
cd ch06\rag_ch06_02
uv run main.py --generate
```

환경 변수는 현재 터미널에만 적용돼요. 새 터미널을 열었다면 다시 지정해요. 모델 응답은 환경과 버전에 따라 달라요.

## 막힐 때

| 증상 | 확인할 것 |
| --- | --- |
| `uv sync` 중 `os error 396` (하드 링크 오류) | OneDrive 동기화 폴더예요. `setx UV_LINK_MODE copy`를 실행하고 터미널을 새로 연 뒤 다시 `uv sync` 해요. 압축을 동기화되지 않는 폴더에 다시 푸는 것도 방법이에요 |
| `FileNotFoundError: embedding_config.json` | 그 강의 폴더에서 `uv run prepare.py`를 먼저 실행해요 |
| `Collection ... already exists` | 같은 실행 안에서 생성 코드만 반복했어요. `uv run main.py`로 파일 전체를 새로 실행해요 |
| client / index가 닫혔다는 오류 | 실습 코드를 `client.close()` / `index.close()` 위로 옮겨요 |
| `--generate`에서 Connection refused | Ollama 앱이 실행 중인지, `OLLAMA_BASE_URL`이 `http://localhost:11434`인지 확인해요 |
| `--generate`에서 model not found | `ollama list`에 나온 태그를 `OLLAMA_MODEL`에 정확히 넣어요 |
| HF 토큰 · symlink · `position_ids UNEXPECTED` 경고 | 모델을 받거나 불러올 때 나오는 안내 문구예요. 실행 결과에는 영향이 없어요 |
| `ModuleNotFoundError` | `rag_day3` 폴더에서 `uv sync`를 했는지, `uv run`으로 실행했는지 확인해요 |
| 강의 폴더에 `pyproject.toml`이 생겼어요 | 실수로 `uv init`을 실행한 거예요. 그 강의 폴더의 `pyproject.toml`, `.python-version`, `.venv`를 지우면 다시 공용 환경을 써요 |

## 검증 기록

- 2026-10-20 · Windows 11 · Python 3.12에서 확인했어요.
- 8개 강의의 `prepare.py`·`main.py`·`solution.py`를 공용 환경으로 실행한 결과가 교안의 "전체 기본 실행 결과"와 같았어요 (예: 5-1 Point ID `7729ce2c-…` · 등록 2번에도 1개, 5-2 Top-3 0.8945 · 0.875 · 0.8444, 5-3 travel-old 0.9003 · 28 → 5, 5-4 3 → 5 → 2, 6-1 예산 120 · 200 · 300 → 69 · 165 · 261자, 6-3 unknown_source · quote_not_found · review_meaning).
- 퀴즈 8개 모두 `q_solution.py`가 통과하고, `q_easy.py` 빈칸을 정답으로 채우면 통과하는 것을 확인했어요.
