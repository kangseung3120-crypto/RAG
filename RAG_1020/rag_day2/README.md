# RAG 2일차 실습 자료 (3장 오전 · 4장 오후)

3장과 4장 강의 8개의 실습 폴더를 하나로 묶었어요. **uv 실행 환경은 이 폴더에 하나만 만들고 8개 강의가 함께 써요.** 그래서 오늘은 처음에 한 번만 세팅하면 돼요.

## 폴더 구성

```
rag_day2/
├─ pyproject.toml      ← 8개 강의에 필요한 패키지 목록 (함께 씀)
├─ uv.lock             ← 패키지 버전 고정 (함께 씀)
├─ .python-version     ← Python 3.12 (함께 씀)
├─ ch03/  (오전)
│  ├─ rag_ch03_01/     3장 1강  Chunk Size와 Overlap
│  ├─ rag_ch03_02/     3장 2강  Fixed/Recursive/Token 청킹
│  ├─ rag_ch03_03/     3장 3강  한국어/문서 구조 기반 청킹
│  └─ rag_ch03_04/     3장 4강  청킹 전략 비교와 선택
└─ ch04/  (오후)
   ├─ rag_ch04_01/     4장 1강  텍스트 임베딩과 벡터 표현
   ├─ rag_ch04_02/     4장 2강  코사인 유사도와 Top-k 검색
   ├─ rag_ch04_03/     4장 3강  Dense Retriever의 Top-k / Threshold
   └─ rag_ch04_04/     4장 4강  임베딩 모델 비교와 Dense 기준선
```

강의 폴더 안의 파일은 노션 교안의 ZIP과 같아요. 여기에 퀴즈 파일 3개(`q_easy.py`, `q_hard.py`, `q_solution.py`)를 더했어요.

## 처음 한 번만: 세팅

1. **압축 풀기:** ZIP을 OneDrive와 동기화되지 않는 곳(예: `C:\rag`)에 풀어요. 바탕 화면이나 문서 폴더가 OneDrive와 동기화돼 있으면 설치 중에 오류가 날 수 있어요.
2. **폴더 열기:** VS Code에서 **파일 → 폴더 열기**로 `rag_day2` 폴더를 열어요. 강의 폴더가 아니라 이 루트 폴더를 열어요.
3. **터미널에서 설치:** **터미널 → 새 터미널**(PowerShell)을 열고 아래를 실행해요.

```powershell
# uv와 Python 3.12가 준비됐는지 확인해요.
uv --version
uv python install 3.12
# 8개 강의에 필요한 패키지를 한 번에 설치해요. rag_day2 폴더에서 실행해요.
uv sync
```

`.venv` 폴더가 `rag_day2` 바로 아래에 하나 생기면 끝이에요. 4장에서 쓰는 PyTorch가 함께 설치돼서 **1일차보다 오래 걸려요(수백 MB).**

4. **임베딩 모델 미리 받기 (오후 수업 전에):** 4장의 E5 모델(`intfloat/multilingual-e5-small`)은 처음 실행할 때 인터넷에서 내려받아요. 쉬는 시간에 한 번 실행해 두면 오후에 기다리지 않아요.

```powershell
cd ch04\rag_ch04_01
uv run check_embedding.py
```

마지막 줄에 `"shape": [2, 384]`가 나오면 준비가 끝났어요. 처음에는 몇 분 걸릴 수 있고, 두 번째부터는 저장된 모델을 써요.

> **교안의 "실습 준비"와 다른 점:** 교안은 강의마다 `uv init`, `uv python pin`, `uv add`를 하라고 안내해요. 이 묶음에서는 위의 `uv sync` 한 번으로 대신하므로, **강의 폴더 안에서 `uv init`을 실행하지 마세요.** 실행하면 그 강의 폴더에만 환경이 따로 생겨요.

## 강의마다: 실행

강의 폴더로 이동한 뒤 교안대로 `uv run`을 실행해요. uv가 상위 폴더의 환경을 자동으로 찾아 써요.

```powershell
# 예: 3장 1강
cd ch03\rag_ch03_01
uv run main.py
uv run solution.py

# 4장 2강부터는 prepare.py로 벡터를 먼저 만들어요.
cd ..\..\ch04\rag_ch04_02
uv run prepare.py
uv run main.py
```

- **4-2, 4-3, 4-4는 `uv run prepare.py`를 먼저 실행해요.** `vectors.npy`와 `embedding_config.json`이 생기고, `main.py`가 이 파일을 읽어요. 먼저 실행하지 않으면 `FileNotFoundError: embedding_config.json`이 나요.
- 강의 폴더마다 교안 "직접 실습" 문제가 세 가지 파일로 들어 있어요. 모두 `main.py`를 먼저 실행한 뒤 문제를 확인해요. 통과하면 `✅ 정답이에요!`가 나와요.
  - `q_easy.py`: 정답 코드에 빈칸(`____`)을 뚫어 둔 버전
  - `q_hard.py`: 교안의 TODO 그대로
  - `q_solution.py`: 교안 정답
- 강의 코드는 자기 폴더의 `documents.json`, `chunks.json`을 읽어요. **반드시 해당 강의 폴더로 이동한 뒤 실행해요.** 다른 위치에서 실행하면 `FileNotFoundError`가 나요.
- 4장 강의는 E5 모델을 불러오느라 실행마다 수십 초 걸려요. 멈춘 게 아니니 기다려요.

## VS Code 편집기 설정 (import 밑줄이 보일 때)

Ctrl+Shift+P → **Python: Select Interpreter** → `rag_day2\.venv\Scripts\python.exe`를 골라요. 8개 강의 모두 이 하나로 돼요.

## 선택 실습: 4장 4강

두 가지 모두 선택이에요. 강의 시간에는 저장된 기록(`recorded_e5_comparison.json`)으로 결과를 확인해요.

```powershell
cd ch04\rag_ch04_04
# E5 base 모델을 추가로 내려받아 small과 같은 조건으로 비교해요 (1GB 안팎).
uv run main.py --compare-base
```

외부 임베딩 API 비교는 교안 README의 순서대로 해요. `uv add openai==2.54.0`을 강의 폴더에서 실행하면 공용 환경(`rag_day2`)에 추가돼요. `--execute`를 붙이지 않으면 API를 호출하지 않아요.

## 막힐 때

| 증상 | 확인할 것 |
| --- | --- |
| `uv sync` 중 `os error 396` (하드 링크 오류) | OneDrive 동기화 폴더예요. `setx UV_LINK_MODE copy`를 실행하고 터미널을 새로 연 뒤 다시 `uv sync` 해요. 압축을 동기화되지 않는 폴더에 다시 푸는 것도 방법이에요 |
| `uv sync`가 오래 걸려요 | PyTorch를 내려받는 중이에요. 네트워크가 느리면 몇 분 걸릴 수 있어요 |
| 4장 첫 실행이 멈춘 것 같아요 | E5 모델을 내려받는 중이에요. `check_embedding.py`로 미리 받아 두면 이후엔 빨라요 |
| 모델 내려받기 중 symlink 경고 | Windows에서 나오는 안내 문구예요. 실행 결과에는 영향이 없어요 |
| `vectors.npy` / `embedding_config.json` 없음 | 4-2~4-4 강의 폴더에서 `uv run prepare.py`를 먼저 실행해요 |
| `FileNotFoundError: documents.json` | 강의 폴더로 이동했는지 `Get-Location`으로 확인해요 |
| `ModuleNotFoundError` | `rag_day2` 폴더에서 `uv sync`를 했는지 확인해요 |
| 강의 폴더에 `pyproject.toml`이 생겼어요 | 실수로 `uv init`을 실행한 거예요. 그 강의 폴더의 `pyproject.toml`, `.python-version`, `.venv`를 지우면 다시 공용 환경을 써요 |

## 검증 기록

- 2026-10-19 · Windows 11 · Python 3.12에서 확인했어요.
- 8개 강의의 `main.py`·`solution.py`·`prepare.py`·`check_embedding.py`를 공용 환경으로 실행한 결과가 교안의 "전체 기본 실행 결과"와 같았어요 (예: 3-2 토큰 청크 51/33, 4-1 shape (28, 384), 4-2 1위 0.8945, 4-3 threshold 0.88에서 2개, 4-4 Hit@3 · Recall@3 1.0).
- 퀴즈 8개 모두 `q_solution.py`가 통과하고, `q_easy.py` 빈칸을 정답으로 채우면 통과하는 것을 확인했어요.
