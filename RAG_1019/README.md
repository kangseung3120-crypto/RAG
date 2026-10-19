# RAG 1일차 실습 자료 (1장 오전 · 2장 오후)

1장과 2장 강의 8개의 실습 폴더를 하나로 묶었어요. **uv 실행 환경은 이 폴더에 하나만 만들고 8개 강의가 함께 써요.** 그래서 오늘은 처음에 한 번만 세팅하면 돼요.

## 폴더 구성

```
rag_day1/
├─ pyproject.toml      ← 8개 강의에 필요한 패키지 목록 (함께 씀)
├─ uv.lock             ← 패키지 버전 고정 (함께 씀)
├─ .python-version     ← Python 3.12 (함께 씀)
├─ ch01/  (오전)
│  ├─ rag_ch01_01/     1장 1강  RAG가 필요한 이유와 적용 조건
│  ├─ rag_ch01_02/     1장 2강  Indexing과 Query 파이프라인
│  ├─ rag_ch01_03/     1장 3강  2-Step RAG 기준선과 실습 환경
│  └─ rag_ch01_04/     1장 4강  RAG와 Long Context, CAG 선택 기준
├─ ch02/  (오후)
│  ├─ rag_ch02_01/     2장 1강  문서 로딩과 Document 구조
│  ├─ rag_ch02_02/     2장 2강  출처 추적을 위한 Metadata 설계
│  ├─ rag_ch02_03/     2장 3강  중복/빈 본문/Boilerplate 정제
└─ rag_ch02_04/     2장 4강  표준 JSONL 저장과 데이터 검수
```

강의 폴더 안의 파일은 노션 교안의 ZIP과 똑같아요.

## 처음 한 번만: 세팅

1. **압축 풀기:** ZIP을 OneDrive와 동기화되지 않는 곳(예: `C:\rag`)에 풀어요. 바탕 화면이나 문서 폴더가 OneDrive와 동기화돼 있으면 설치 중에 오류가 날 수 있어요.
2. **폴더 열기:** VS Code에서 **파일 → 폴더 열기**로 `rag_day1` 폴더를 열어요. 강의 폴더가 아니라 이 루트 폴더를 열어요.
3. **터미널에서 설치:** **터미널 → 새 터미널**(PowerShell)을 열고 아래를 실행해요.

```powershell
# uv와 Python 3.12가 준비됐는지 확인해요.
uv --version
uv python install 3.12
# 8개 강의에 필요한 패키지를 한 번에 설치해요. rag_day1 폴더에서 실행해요.
uv sync
```

`.venv` 폴더가 `rag_day1` 바로 아래에 하나 생기면 끝이에요.

> **교안의 "실습 준비"와 다른 점:** 교안은 강의마다 `uv init`, `uv python pin`, `uv add`를 하라고 안내해요. 이 묶음에서는 위의 `uv sync` 한 번으로 대신하므로, **강의 폴더 안에서 `uv init`이나 `uv add`를 실행하지 마세요.** 실행하면 그 강의 폴더에만 환경이 따로 생겨요.

## 강의마다: 실행

강의 폴더로 이동한 뒤 교안대로 `uv run`을 실행해요. uv가 상위 폴더의 환경을 자동으로 찾아 써요.

```powershell
# 예: 1장 1강
cd ch01\rag_ch01_01
uv run main.py

# 다음 강의로 갈 때는 rag_day1에서 다시 이동해요.
cd ..\..\ch02\rag_ch02_03
uv run main.py
uv run solution.py
```

- 강의 폴더마다 교안 "직접 실습" 문제가 세 가지 파일로 들어 있어요. 모두 `main.py`를 먼저 실행한 뒤 문제를 확인해요. 통과하면 `✅ 정답이에요!`가 나와요.
  - `q_easy.py`: 정답 코드에 빈칸(`____`)을 뚫어 둔 버전
  - `q_hard.py`: 교안의 TODO 그대로
  - `q_solution.py`: 교안 정답
- 강의 코드는 자기 폴더의 `documents.json`, `raw/`를 읽어요. **반드시 해당 강의 폴더로 이동한 뒤 실행해요.** 다른 위치에서 실행하면 `FileNotFoundError`가 나요.
- `documents.json`은 8개 강의 모두 같은 내용의 사본이에요. 교안 코드를 그대로 실행할 수 있도록 강의 폴더마다 하나씩 들어 있어요.

## VS Code 편집기 설정 (import 밑줄이 보일 때)

Ctrl+Shift+P → **Python: Select Interpreter** → `rag_day1\.venv\Scripts\python.exe`를 골라요. 8개 강의 모두 이 하나로 돼요.

## 선택 실습: 1장 3강 Ollama 답변 생성

`httpx`는 이미 설치돼 있어서 `uv add`는 필요 없어요. Ollama 설치와 모델 준비만 하면 돼요.

```powershell
ollama pull gemma3:4b-it-q4_K_M
cd ch01\rag_ch01_03
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "gemma3:4b-it-q4_K_M"
uv run generate_answer.py
```

## 막힐 때

| 증상 | 확인할 것 |
| --- | --- |
| `uv sync` 중 `os error 396` (하드 링크 오류) | OneDrive 동기화 폴더예요. `setx UV_LINK_MODE copy`를 실행하고 터미널을 새로 연 뒤 다시 `uv sync` 해요. 압축을 동기화되지 않는 폴더에 다시 푸는 것도 방법이에요. 예전에 OneDrive 폴더에서 uv를 쓴 적이 있으면 다른 폴더로 옮겨도 같은 오류가 날 수 있어요(uv 캐시가 OneDrive와 묶인 경우). 이때도 `setx UV_LINK_MODE copy`로 해결돼요 |
| `FileNotFoundError: documents.json` | 강의 폴더로 이동했는지 `Get-Location`으로 확인해요 |
| `ModuleNotFoundError: pypdf` / `langchain_core` | `rag_day1` 폴더에서 `uv sync`를 했는지 확인해요 |
| 강의 폴더에 `pyproject.toml`이 생겼어요 | 실수로 `uv init`을 실행한 거예요. 그 강의 폴더의 `pyproject.toml`, `.python-version`, `.venv`를 지우면 다시 공용 환경을 써요 |

## 검증 기록

- 2026-10-18 · Windows 11 · uv 0.13.0 · Python 3.12.15에서 확인했어요.
- 8개 강의의 `main.py`·`solution.py` 12개를 공용 환경으로 실행한 결과가, 교안 방식(강의마다 `uv init`)으로 실행한 결과와 글자 하나까지 같았어요.
- 1장 3강 `generate_answer.py`(Ollama `gemma3:4b-it-q4_K_M`)도 정상적으로 실행됐어요.
